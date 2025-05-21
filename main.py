import pandas as pd
import streamlit as st
from st_aggrid import AgGrid
from make_aggrid import make_grid
from utils import adjust_coluns
import plotly.graph_objects as go

def show():

    def make_aggrid(df):
        return AgGrid(
        df,
        gridOptions=grid_options,
        enable_enterprise_modules=False,
        fit_columns_on_grid_load=True,
        allow_unsafe_jscode=True,
        height=300    
    )

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
    st.image(r'D:\HILTI\images\hilti logos\logoHilti.png')
    st.markdown('</div>', unsafe_allow_html=True)

    st.title('Rental Dash - Tool Life Time')
    st.divider()

    df_over_view = pd.read_csv(r'C:\Users\Eduardo\OneDrive - Hilti\Rental Dash\CC Sorocaba\Tools with repairs info.csv')

    df_over_view = adjust_coluns(df_over_view)

    grid_options = make_grid(df_over_view)

    grid_response_over_view = make_aggrid(df_over_view)

    df_over_view_response = grid_response_over_view.data
    selected_rows_over_view_response = grid_response_over_view.selected_rows

    if selected_rows_over_view_response is not None and not selected_rows_over_view_response.empty:
        st.divider()
        # st.dataframe(selected_rows_over_view_response)
        serial_number = selected_rows_over_view_response.iloc[0, 1]

        df_tool_type_deep_dive = pd.read_csv(r'C:\Users\Eduardo\OneDrive - Hilti\Rental Dash\CC Sorocaba\G_GMRRPCOPA_AMS_KF2_W2.csv')
        df_tool_type_deep_dive = adjust_coluns(df_tool_type_deep_dive)
        df_tool_type_deep_dive = df_tool_type_deep_dive.loc[df_tool_type_deep_dive['(n) Serial Number'] == serial_number]
        # st.dataframe(df_tool_type_deep_dive)

        data_compra = pd.to_datetime(selected_rows_over_view_response.iloc[0, 4])
        ferramenta = selected_rows_over_view_response.iloc[0, 2]

        linha_vida = pd.concat([
            pd.DataFrame({'data': [data_compra], 'Total Cust': [0]}),
            df_tool_type_deep_dive.rename(columns={'Notif. Completion Date': 'data'})[['data', 'Total Cust']]
        ]).sort_values('data')

        # Criar o gráfico
        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=linha_vida['data'],
            y=linha_vida['Total Cust'],
            mode='lines+markers',
            marker=dict(size=10),
            line=dict(color='red'),
            name='Custo de Reparo'
        ))

        fig.update_layout(
            title=f"Life Time {ferramenta} serial number: {serial_number}",
            xaxis_title='Data',
            yaxis_title='Custo (R$)',
            xaxis=dict(showgrid=True),
            yaxis=dict(showgrid=True),
            hovermode='x unified'
        )

        st.plotly_chart(fig, use_container_width=True)    