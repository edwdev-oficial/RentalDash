import pandas as pd
import streamlit as st
from st_aggrid import AgGrid
from make_aggrid import make_grid
from utils import adjust_coluns
import plotly.graph_objects as go
import gspread

def load_data():
    gc = gspread.service_account_from_dict(st.secrets["gspread_service_account"])
    sh_tools_with_repairs_info = gc.open('Tools with repairs info')
    df_over_view = pd.DataFrame(
        sh_tools_with_repairs_info.worksheet('Sheet1').get_all_values()[1:],
        columns = sh_tools_with_repairs_info.worksheet('Sheet1').get_all_values()[0]
    )
    sh_G_GMRRPCOPA_AMS_KF2_W2 = gc.open('G_GMRRPCOPA_AMS_KF2_W2')
    df_tool_type_deep_dive = pd.DataFrame(
        sh_G_GMRRPCOPA_AMS_KF2_W2.worksheet('Sheet1').get_all_values()[1:],
        columns = sh_G_GMRRPCOPA_AMS_KF2_W2.worksheet('Sheet1').get_all_values()[0]
    )
    df_over_view = adjust_coluns(df_over_view)
    df_tool_type_deep_dive = adjust_coluns(df_tool_type_deep_dive)

    return {'df_over_view': df_over_view, 'df_tool_type_deep_dive': df_tool_type_deep_dive}

def make_aggrid(df, grid_options):
    return AgGrid(
    df,
    gridOptions=grid_options,
    enable_enterprise_modules=False,
    fit_columns_on_grid_load=True,
    allow_unsafe_jscode=True,
    height=300    
)

def show():

    #%% logo
    st.markdown("""
        <style>
        .streamlit-expanderHeader {
            border-radius: 0 !important;
        }
        img {
            border-radius: 0 !important;
        }
        </style>
    """, unsafe_allow_html=True)
    # Injetar CSS para alinhar a imagem à direita
    st.markdown("""
        <style>
        .right-align {
            text-align: right;
        }
        </style>
    """, unsafe_allow_html=True)
    st.markdown('<div class="right-align">', unsafe_allow_html=True)
    st.image('assets/imgs/logoHilti.png')
    st.markdown('</div>', unsafe_allow_html=True)

    #%% Title
    st.title('Rental Dash - Tool Life Time')
    st.divider()

    if 'loaded_data' not in st.session_state:
        st.session_state.loaded_data = load_data()

    dados = st.session_state.loaded_data

    df_over_view = dados['df_over_view']
    df_tool_type_deep_dive = dados['df_tool_type_deep_dive']
    grid_options = make_grid(df_over_view)
    grid_response_over_view = make_aggrid(df_over_view, grid_options)

    selected_rows_over_view_response = grid_response_over_view.selected_rows

    if selected_rows_over_view_response is not None and not selected_rows_over_view_response.empty:
        serial_number = selected_rows_over_view_response.iloc[0, 1]

        df_tool_type_deep_dive = df_tool_type_deep_dive.loc[df_tool_type_deep_dive['(n) Serial Number'] == serial_number].copy()

        data_compra = pd.to_datetime(selected_rows_over_view_response.iloc[0, 4])
        ferramenta = selected_rows_over_view_response.iloc[0, 2]

        df_tool_type_deep_dive['Notif. Completion Date'] = pd.to_datetime(df_tool_type_deep_dive['Notif. Completion Date'], errors='coerce')

        linha_vida = pd.concat([
            pd.DataFrame({'data': [data_compra], 'Total Cust': [0]}),
            df_tool_type_deep_dive.rename(columns={'Notif. Completion Date': 'data'})
        ]).sort_values('data')
        # st.dataframe(linha_vida)
        linha_vida['Cost per repair'] = round(pd.to_numeric(linha_vida['Total Cust'], errors='coerce'), 2)
        linha_vida['Total Covered by Customer'] = round(linha_vida['Covered by Customer'].cumsum(), 2)

        # Criar o gráfico
        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=linha_vida['data'],
            y=linha_vida['Cost per repair'],
            mode='lines+markers',
            marker=dict(size=10),
            line=dict(color='red'),
            name='Cost per repair'
        ))


        fig.add_trace(go.Scatter(
            x=linha_vida['data'],
            y=linha_vida['Total Covered by Customer'],
            mode='lines+markers',
            marker=dict(size=8),
            line=dict(color='blue', dash='dash'),
            name='Total Covered by Customer'
        ))

        fig.update_layout(
            title=f"Life Time {ferramenta} serial number: {serial_number}",
            xaxis_title='Data',
            yaxis_title='Custo (R$)',
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True),
            hovermode='x unified'
        )

        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Selecione uma ferramenta na tabela acima para ver o gráfico de vida útil.")  

