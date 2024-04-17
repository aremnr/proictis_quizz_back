# Тут расписаны все endpoint-ы


## Добавление 

<table>
    <tr>
        <th>ecndpoint</th>
        <th>Назначение</th>
        <th>Параметры</th>
    </tr>
    <tr>
        <td>/quiz/add</td>
        <td>Добаление квиза со всеми вопросами и ответами на них</td>
        <td></td>
    </tr>
    <tr>
        <td>/quiz/{quiz_id}/add/question</td>
        <td>Добавление вопроса со всеми ответами в определенный квиз</td>
        <td>quiz_id - str(uuid)</td>
    </tr>
    <tr>
        <td>/quiz/{quiz_id}/{question_id}/add</td>
        <td>Добавление ответа в определенный вопрос</td>
        <td>quiz_id - str(uuid)<br>question_id - str(uuid)</td>
    </tr>
</table>


### Пример ТЕЛО запроса
### **ВАЖНО: поля id/quiz_id/question_id могут иметь любое строковое значение в теле запроса(но не в пути)**

#### /quiz/add

```json
{
  "quiz": {
    "id": "string",
    "name": "string",
    "dis": "string",
    "question_count": 0,
    "owner_id": "string",
    "all_points": 0
  },
  "qestions": {
    "list": [
      {
        "id": "string",
        "quiz_id": "string",
        "question_text": "string",
        "points": 0,
        "right_answer": 0,
        "pcl": 0,
        "answers_list": {
          "list": [
            {
              "id": "string",
              "question_id": "string",
              "answer_text": "string"
            }
          ]
        }
      }
    ]
  }
}
```


#### /quiz/{quiz_id}/add/question

```json
{
  "id": "string",
  "quiz_id": "string",
  "question_text": "string",
  "points": 0,
  "right_answer": 0,
  "pcl": 0,
  "answers_list": {
    "list": [
      {
        "id": "string",
        "question_id": "string",
        "answer_text": "string"
      }
    ]
  }
}
```

#### /quiz/{quiz_id}/{question_id}/add

```json
{
  "id": "string",
  "question_id": "string",
  "answer_text": "string"
}
```


## Получение

<table>
    <tr>
        <th>ecndpoint</th>
        <th>Назначение</th>
        <th>Параметры</th>
    </tr>
    <tr>
        <td>/quiz/{quiz_id}</td>
        <td>Получить данные квиза</td>
        <td>quiz_id - str(uuid)</td>
    </tr>
    <tr>
        <td>/quiz/{quiz_id}/question</td>
        <td>Получить вопрос со всеми ответами</td>
        <td>quiz_id - str(uuid)<br>query параметр question_number - int(default = 0)</td>
    </tr>
</table>

## Удаление

<table>
    <tr>
        <th>ecndpoint</th>
        <th>Назначение</th>
        <th>Параметры</th>
    </tr>
    <tr>
        <td>/quiz/del/quiz/{quiz_id}</td>
        <td>Удаление квиза со всеми вопросами и ответами на них</td>
        <td>quiz_id - str(uuid)</td>
    </tr>
    <tr>
        <td>/quiz/del/question/{question_id}</td>
        <td>Удаление вопроса со всеми ответами</td>
        <td>question_id - str(uuid)</td>
    </tr>
    <tr>
        <td>/quiz/del/answer/{answer_id}</td>
        <td>Удаление ответа определенного вопроса</td>
        <td>answer_id - str(uuid)</td>
    </tr>
</table>


---
Развертывание приложения
---
<br>
Postgresql: <br>

```bash
docker run -p 5432:5432 --name pg_trading -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=postgres -d postgres:13.3
```

Приложение: <br>
```bash
docker build . --tag quiz_app && docker run -p 80:8081 quiz_app 
```