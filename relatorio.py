"""Geração de relatórios executivos (Excel e PDF) da carteira de corretores.

Mesma lógica de formatação que já existia em relatorio_model.py, apenas
reorganizada como uma classe de serviço (RelatorioService), no mesmo
espírito dos repositórios: agrupa em um objeto tudo o que pertence a essa
responsabilidade, em vez de funções soltas no módulo.
"""

class RelatorioService:
    COR_AZUL = (33, 78, 120)

    def __init__(self):
        self.output_dir = os.path.join(os.path.dirname(__file__), "relatórios")
        os.makedirs(self.output_dir, exist_ok=True)

    def _timestamp(self):
        return datetime.now().strftime("%Y%m%d_%H%M%S")

    def _consultar_corretores(self, colunas):
        conexao = Conexao.nova_conexao_bruta()
        try:
            query = f"SELECT {colunas} FROM Corretor"
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                return pd.read_sql(query, conexao)
        finally:
            conexao.close()

    def exportar_corretores_excel(self):
        try:
            df = self._consultar_corretores("id_corretor, nome, creci, telefone, email")
            df.columns = ["ID", "Nome Completo", "CRECI", "Telefone", "E-mail"]

            filename = os.path.join(self.output_dir, f"Relatorio_Corretores_{self._timestamp()}.xlsx")

            with pd.ExcelWriter(filename, engine="openpyxl") as writer:
                df.to_excel(writer, sheet_name="Corretores", index=False)
                worksheet = writer.sheets["Corretores"]

                header_fill = PatternFill(start_color="1F4E78", end_color="1F4E78", fill_type="solid")
                header_font = Font(name="Arial", size=11, bold=True, color="FFFFFF")
                zebra_fill = PatternFill(start_color="F2F5F8", end_color="F2F5F8", fill_type="solid")
                data_font = Font(name="Arial", size=10)
                thin_border = Border(
                    left=Side(style="thin", color="DDDDDD"), right=Side(style="thin", color="DDDDDD"),
                    top=Side(style="thin", color="DDDDDD"), bottom=Side(style="thin", color="DDDDDD"),
                )

                for col_idx, col in enumerate(df.columns, start=1):
                    cell = worksheet.cell(row=1, column=col_idx)
                    cell.fill = header_fill
                    cell.font = header_font
                    cell.alignment = Alignment(horizontal="left" if col_idx > 1 else "center", vertical="center")

                for row_idx in range(2, worksheet.max_row + 1):
                    is_even = row_idx % 2 == 0
                    for col_idx in range(1, worksheet.max_column + 1):
                        cell = worksheet.cell(row=row_idx, column=col_idx)
                        cell.font = data_font
                        cell.border = thin_border
                        if is_even:
                            cell.fill = zebra_fill
                        cell.alignment = Alignment(horizontal="center" if col_idx == 1 else "left")

                for col in worksheet.columns:
                    max_len = max(len(str(cell.value or "")) for cell in col)
                    col_letter = col[0].column_letter
                    worksheet.column_dimensions[col_letter].width = max(max_len + 3, 12)

            print(f"\n✅ Planilha executiva '{filename}' gerada com sucesso!")
        except Exception as e:
            print(f"\n❌ Erro ao gerar planilha: {e}")

    def exportar_corretores_pdf(self):
        try:
            df = self._consultar_corretores("id_corretor, nome, creci, email")

            pdf = FPDF()
            pdf.add_page()

            pdf.set_font("Arial", style="B", size=20)
            pdf.set_text_color(*self.COR_AZUL)
            pdf.cell(190, 10, txt="Alleanza Immobiliare", ln=True, align="L")

            pdf.set_font("Arial", size=10)
            pdf.set_text_color(100, 100, 100)
            pdf.cell(190, 5, txt="Relatorio Executivo de Corretores Cadastrados", ln=True, align="L")
            pdf.ln(5)

            pdf.set_draw_color(*self.COR_AZUL)
            pdf.set_line_width(0.5)
            pdf.line(10, pdf.get_y(), 200, pdf.get_y())
            pdf.ln(10)

            pdf.set_font("Arial", style="B", size=10)
            pdf.set_text_color(255, 255, 255)
            pdf.set_fill_color(*self.COR_AZUL)

            pdf.cell(15, 8, "ID", border=1, align="C", fill=True)
            pdf.cell(65, 8, "Nome Completo", border=1, align="L", fill=True)
            pdf.cell(40, 8, "Inscricao CRECI", border=1, align="L", fill=True)
            pdf.cell(70, 8, "E-mail de Contato", border=1, align="L", fill=True)
            pdf.ln()

            pdf.set_font("Arial", size=9)
            pdf.set_text_color(0, 0, 0)

            for idx, row in df.iterrows():
                if idx % 2 == 0:
                    pdf.set_fill_color(242, 245, 248)
                else:
                    pdf.set_fill_color(255, 255, 255)

                pdf.cell(15, 7, str(row["id_corretor"]), border=1, align="C", fill=True)
                pdf.cell(65, 7, str(row["nome"]), border=1, align="L", fill=True)
                pdf.cell(40, 7, str(row["creci"]), border=1, align="L", fill=True)
                pdf.cell(70, 7, str(row["email"]), border=1, align="L", fill=True)
                pdf.ln()

            pdf_filename = os.path.join(self.output_dir, f"Relatorio_Corretores_{self._timestamp()}.pdf")
            pdf.output(pdf_filename)
            print(f"\n✅ Documento PDF Executivo '{pdf_filename}' gerado com sucesso!")
        except Exception as e:
            print(f"\n❌ Falha ao compilar PDF: {e}")