import json


extracted_txt = open("extracted_text.txt", "r", encoding="utf-8")

questions = dict({
  "modules": {}
})

for line in extracted_txt:
  if len(line.strip()) == 0 or line.startswith("CNH do Brasil") or line.startswith("Respostas incorretas:") or line.startswith("BANCO") or line.startswith(" PARTE") or line.startswith(" QUESTÕES") or line.startswith(" Versão") :
    continue

  if line.startswith("MÓDULO"):
    module_number = line.split(" ")[1]
    print(f"Processing module {module_number}")

    if module_number not in questions["modules"]:
      module_title = line.split(" - ")[1].strip()
      questions["modules"][module_number] = {
        "title": module_title,
        "questions": []
      }
    
  if line.startswith("●"):
    ## Exemplo de questão: ● (Fácil) 1. Ao ver a placa de “Área Escolar”, o que o motorista deve fazer?
    ## Dificuldade: Fácil
    ## Título: Ao ver a placa de “Área Escolar”, o que o motorista deve fazer?
    ## Número da questão: 1

    question_text = line[1:].strip()
    question_title = question_text.split(".")[1].strip()
    question_difficulty = question_text.split(")")[0].strip(" (")
    question_number = int(question_text.split(".")[0].split(" ")[-1])
    # questions_length = len(questions["modules"][module_number]["questions"])

    questions["modules"][module_number]["questions"].append({
      "title": question_title,
      "difficulty": question_difficulty,
      "number": question_number,
      "answers": []
    })
  
  question_index = next((index for (index, d) in enumerate(questions["modules"][module_number]["questions"]) if d["title"] == question_title and d["number"] == question_number and d["difficulty"] == question_difficulty), None)

  if line.startswith("Código da placa:"):
    ## Exemplo de código da placa: Código da placa: ABX-1234
    sign_code = line.split(":")[1].strip()
    questions["modules"][module_number]["questions"][question_index]["sign_code_ref"] = sign_code

  if line.startswith("Alternativa correta:"):
    ## Exemplo de alternativa correta: Alternativa correta: Sinalizar a manobra antes de virar. ✓
    correct_answer = line.split(":")[1].strip().rstrip("✓").strip()
    questions["modules"][module_number]["questions"][question_index]['answers'].append({
      "text": correct_answer,
      "is_correct": True
    })

  if line.startswith("Comentário:"):
    ## Exemplo de comentário: Comentário: Sinalizar a manobra é obrigatório para garantir a segurança no trânsito.
    comment_text = line.split(":")[1].strip()
    questions["modules"][module_number]["questions"][question_index]['explanation'] = comment_text

  if line.startswith("   ✗ "):
    ## Exemplo de alternativa incorreta:    ✗ Deixar de usar o cinto de segurança.
    incorrect_answer = line.strip("✗ ").strip()
    questions["modules"][module_number]["questions"][question_index]['answers'].append({
      "text": incorrect_answer,
      "is_correct": False
    })

print(questions)
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