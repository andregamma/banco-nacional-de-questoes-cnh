from pypdf import PdfReader

# Cria o arquivo de texto para armazenar o conteúdo extraído
final_txt = open("extracted_text.txt", "w", encoding="utf-8")

print("Realizando leitura do arquivo único")
reader = PdfReader("Banco Nacional de Questões.pdf")

## Verifica quantidade de páginas
pages_count = len(reader.pages)
print(f"Número de páginas: {pages_count}")
for i in range(pages_count):
  page = reader.pages[i]
  # Inclui o texto extraído no arquivo
  final_txt.write(page.extract_text() + "\n\n")
  
final_txt.close()
print("Extração concluída. Texto salvo em 'extracted_text.txt'.")

