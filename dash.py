import streamlit as st
import pandas as pd
import plotly.express as px


    # Configuration de la page
    
st.set_page_config(page_title="KPIs du réseau mobile",
                   page_icon=":bar_chart:")
   
   
def load_excel_data(uploaded_file):
    df = pd.read_excel(uploaded_file)
    return df

def dashboard():
    # CSS for the background
    with open("index.html", "r") as f:
        html_code = f.read()
    st.components.v1.html(html_code)
    with open("style.css", "r") as f:
        css_code = f.read()
    st.markdown(f"<style>{css_code}</style>", unsafe_allow_html=True)
    st.title("Le tableau de bord des KPIs du réseau mobile")
    # Upload Excel file
    st.sidebar.subheader("Télécharger un fichier Excel")
    uploaded_file = st.sidebar.file_uploader("Sélectionner un fichier Excel", type=["xls", "xlsx"])

    if uploaded_file is not None:
        df = load_excel_data(uploaded_file)

        # afficher data du fichier excel sous forme de tableau
        st.subheader("Fichier Excel")
        st.write(df)

        # Exclude the first column from the column selection for the graph
        column_options = df.columns[1:].tolist()

        # Select l'axe y columns by the user
        st.sidebar.subheader("Sélectionner le(s) KPI(s) à afficher en fonction de la date:")
        selected_columns_y = st.sidebar.multiselect("KPIs", column_options)

        if not selected_columns_y:
            st.sidebar.warning("Veuillez sélectionner au moins un KPI.")
            st.stop()  # Stop execution if no column is selected!

        # Select axis des x column (first column named "DATE/TIME")
        x_column = df.columns[0]

                # Allow the user to create another graph with custom x and y axe
        st.sidebar.subheader("Créer un graphe supplémentaire:")
        x_column_suppl = st.sidebar.selectbox("Sélectionner le KPI 1", column_options)
        y_column_suppl = st.sidebar.selectbox("Sélectionner le KPI2", column_options)

        if x_column_suppl and y_column_suppl:
            fig_suppl = px.line(df, x=x_column_suppl, y=y_column_suppl, title=f"Courbe de {y_column_suppl} en fonction de {x_column_suppl}")
            st.subheader(f"Courbe de {y_column_suppl} en fonction de {x_column_suppl}")
            st.plotly_chart(fig_suppl)

        # Allow the user to select a value on the y axe
        selected_y_value = st.sidebar.number_input("Sélectionner une valeur pour le KPI", min_value=df[selected_columns_y].min().min(), max_value=df[selected_columns_y].max().max())

        if selected_y_value is not None:
            # Filter data based on the selected valeur pour y axe 
            filtered_df = df[df[selected_columns_y] >= selected_y_value]
            st.subheader(f"Éléments ayant une valeur égale à ou supérieure à {selected_y_value} pour les colonnes {', '.join(selected_columns_y)}")

            # Include other columns corresponding to the selected y-axis value
            other_columns = df.columns.difference(selected_columns_y + [x_column])
            st.write(filtered_df[[x_column] + selected_columns_y + list(other_columns)])

        # Allow the user to afficher les top KPIs based on selected columns
        st.sidebar.subheader("Les TOP KPIs:")
        top_kpis = st.sidebar.number_input("Nombre de TOP KPIs", min_value=1, max_value=len(df.columns)-1, value=5)

        if top_kpis:
            # Sort data by the selected columns and select top KPIs
            top_kpis_df = df.nlargest(top_kpis, columns=selected_columns_y)
            st.subheader(f"TOP {top_kpis} KPIs par {', '.join(selected_columns_y)}")
            st.write(top_kpis_df)



   










































          # à propos de l'app
    st.sidebar.title("À Propos")
    st.sidebar.info("Cette application est conçue pour afficher des graphiques interactifs à partir d'un fichier Excel téléchargé. Vous pouvez sélectionner les colonnes que vous souhaitez afficher sur les graphes les KPIs du réseau mobile en fonction des dates données dans le fichiers excel.")
    st.sidebar.info("Cette application a été réalisée à l'aide des bibliothèques Pandas, Plotly Express et Streamlit")
          # Guide d'utilisation
    st.subheader("Guide d'Utilisation:")
    st.write("1. Commencez par télécharger un fichier Excel à partir de la barre latérale.")
    st.write("2. Le fichier sera affiché sous forme de tableau dans la section principale.")
    st.write("3. Sélectionnez une ou plusieurs colonnes dans la barre latérale pour afficher les graphiques en fonction de la date.")
    st.write("4. Vous pouvez également créer un graphe supplémentaire en sélectionnant des axes x et y supplémentaires dans la barre latérale.")
    st.write("5. Amusez-vous avec les graphiques interactifs !")
    # Copyright and Contact Info
    st.sidebar.markdown("---")
    st.sidebar.markdown("© 2023 MAAROF MERIEM. Tous droits réservés.")
    st.sidebar.markdown("Pour plus d'informations sur le code, contactez-moi à mon email : maarofmeriem@gmail.com")











































if __name__ == "__main__":
     dashboard()