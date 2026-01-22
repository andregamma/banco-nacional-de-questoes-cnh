import json


extracted_txt = open("extracted_text.txt", "r", encoding="utf-8")

questions = dict({
  "modules": {}
})

current_prop = None # Propriedade atual sendo processada. Pode ser "question_title", "explanation", "correct_answer", "incorrect_answer"
question_index = None


for line in extracted_txt:
  if len(line.strip()) == 0 or line.startswith("CNH do Brasil") or line.startswith("Respostas incorretas:") or line.startswith("BANCO") or line.startswith(" PARTE") or line.startswith(" QUESTÕES") or line.startswith(" Versão") :
    continue

  print("-----")
  print(f"Processando linha: \"{line.strip()}\"")
  print("Propriedade atual:", current_prop)
  print("Índice da questão atual:", question_index)

  if line.startswith("MÓDULO"):
    module_number = line.split(" ")[1]
    print(f"Processing module {module_number}")

    if module_number not in questions["modules"]:
      module_title = line.split(" - ")[1].strip()
      questions["modules"][module_number] = {
        "title": module_title,
        "questions": []
      }
    continue;

  if line.startswith("●"):
    current_prop = "question_title"
    ## Exemplo de questão: ● (Fácil) 1. Ao ver a placa de “Área Escolar”, o que o motorista deve fazer?
    ## Dificuldade: Fácil
    ## Título: Ao ver a placa de “Área Escolar”, o que o motorista deve fazer?
    ## Número da questão: 1

    question_text = line[1:].strip()
    # Extrai o título da questão. O título é tudo após o número da questão. Considerando que podem haver pontos no título, pegamos tudo após o primeiro ponto.
    question_title = question_text.split(".", 1)[1].strip()
    question_difficulty = question_text.split(")")[0].strip(" (")
    question_number = int(question_text.split(".")[0].split(" ")[-1])

    questions["modules"][module_number]["questions"].append({
      "title": question_title,
      "difficulty": question_difficulty,
      "number": question_number,
      "answers": []
    })

    # Toda vez que uma nova questão for adicionada, atualiza o índice da questão atual para os próximos processamentos.
    question_index = question_index = next((index for (index, d) in enumerate(questions["modules"][module_number]["questions"]) if d["title"] == question_title and d["number"] == question_number and d["difficulty"] == question_difficulty), None)
    continue;

  if line.startswith("Código da placa:"):
    ## Exemplo de código da placa: Código da placa: ABX-1234
    sign_code = line.split(":")[1].strip()
    questions["modules"][module_number]["questions"][question_index]["sign_code_ref"] = sign_code
    continue;

  if line.startswith("Alternativa correta:"):
    ## Exemplo de alternativa correta: Alternativa correta: Sinalizar a manobra antes de virar. ✓
    correct_answer = line.split(":")[1].strip().rstrip("✓").strip()
    current_prop = "correct_answer"
    questions["modules"][module_number]["questions"][question_index]['answers'].append({
      "text": correct_answer,
      "is_correct": True
    })
    continue;

  if line.startswith("Comentário:"):
    ## Exemplo de comentário: Comentário: Sinalizar a manobra é obrigatório para garantir a segurança no trânsito.
    comment_text = line.split(":")[1].strip()
    current_prop = "explanation"
    questions["modules"][module_number]["questions"][question_index]['explanation'] = comment_text
    continue;

  if line.startswith("   ✗ "):
    ## Exemplo de alternativa incorreta:    ✗ Deixar de usar o cinto de segurança.
    incorrect_answer = line.strip("✗ ").strip()
    current_prop = "incorrect_answer"
    questions["modules"][module_number]["questions"][question_index]['answers'].append({
      "text": incorrect_answer,
      "is_correct": False
    })
    continue;
  
  # Gerenciamento de quebras de linha dentro das propriedades
  # Continua a linha anterior (pode ser título da questão, comentário ou alternativa correta)
  if current_prop is not None:
    if current_prop == "question_title":
      questions["modules"][module_number]["questions"][question_index]['title'] += " " + line.strip()
    elif current_prop == "explanation":
      questions["modules"][module_number]["questions"][question_index]['explanation'] += " " + line.strip()
    elif current_prop == "correct_answer":
      last_answer_index = len(questions["modules"][module_number]["questions"][question_index]['answers']) - 1
      correct_answer = line.strip().rstrip("✓").strip()
      questions["modules"][module_number]["questions"][question_index]['answers'][last_answer_index]['text'] += " " + correct_answer
  continue

extracted_txt.close()

with open('questions.json', 'w', encoding='utf-8') as json_file:
    json_file.write(json.dumps(questions, ensure_ascii=False, indent=2))

# Printa estatísticas com número de módulos, questões e alternativas de respostas.
total_modules = len(questions["modules"])
total_questions = sum(len(module["questions"]) for module in questions["modules"].values())
total_answers = sum(len(question["answers"]) for module in questions["modules"].values() for question in module["questions"])

print(f"Total de módulos: {total_modules}")
print(f"Total de questões: {total_questions}")
print(f"Total de alternativas de respostas: {total_answers}")