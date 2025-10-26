from shiny import ui, module, reactive, render
from pathlib import Path
import pandas as pd

@module.ui
def tpm_ui():
    return ui.page_sidebar(
        ui.sidebar(
            ui.input_selectize(
                "sample_selectize",
                "Select Sample(s)", # TODO update to samples
                choices=["A", "B"],
                multiple=True
            ),
        ),
        ui.card(
            ui.card_header("Gene Counts Summary"),
            ui.output_data_frame("render_gene_counts_summary")
        ),
        ui.card(
            ui.card_header("Gene Counts"),
            ui.output_data_frame("render_gene_counts")
        )
    )


@module.server
def tpm_server(input, output, server, samples):
    gene_counts_path = Path("outputs/gene_counts.tsv")
    gene_counts_summary_path = Path("outputs/gene_counts.tsv.summary")

    # print("poop")

    @reactive.effect
    def _():
        sample_names = list(samples())
        ui.update_selectize("sample_selectize", choices=sample_names)

    # FIXME more gracefully handle no file
    @reactive.calc
    def get_gene_counts():
        df = pd.read_csv(gene_counts_path, comment="#", delimiter="\t")
        df = df.drop(columns=["Start", "End", "Strand", "Length", "Chr"])
        df.columns = ["Geneid"] + list(samples())

        for sample in samples():
            df[sample] = df[sample]/df[sample].sum()*1000000
        return df

        
    @reactive.calc
    def get_gene_counts_summary():
        try:
            df = pd.read_csv(gene_counts_summary_path, comment="#", delimiter="\t")
            df.columns = ["Status"] + list(samples())
            return df
        except:
            return
        
    @render.data_frame
    def render_gene_counts_summary():
        try:
            return get_gene_counts_summary()
        except:
            return
        
    # FIXME doesn't work if user examines tab before pipeline is done
    @render.data_frame
    def render_gene_counts():
        df = get_gene_counts()
        if df.empty: return df

        df = df.sort_values(by=df.columns[1], ascending=False)
        if len(input.sample_selectize()) == 0: return df

        selected = [df.columns[0]] + list(input.sample_selectize())

        return render.DataTable(df[selected])


        
