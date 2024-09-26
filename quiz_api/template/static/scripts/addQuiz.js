let questionCount = JSON.parse(localStorage.getItem("QuestionLength"));
function setLocalParams() {
    const quizTitle = document.getElementById('quiz-title').value;
    const quizDescription = document.getElementById('quiz-description').value;
    const quizData = {
        title: quizTitle,
        description: quizDescription,
    };
    const questions = []
    localStorage.setItem("Quiz", JSON.stringify(quizData));
    localStorage.setItem("Questions", JSON.stringify(questions));
    localStorage.setItem("QuestionLength", JSON.stringify(0))
}

function addQuestion() {
    questionCount++;

    const questionContainer = document.createElement('div');
    questionContainer.className = 'question-container';
    questionContainer.id = `question-container-${questionCount}`;

    const questionHTML = `
        <div class ="field">
            <div class="textPos">
                <label class="text" for="question-${questionCount}">Вопрос ${questionCount}</label><br>
            </div>
            <input class="TextField" type="text" id="question-${questionCount}" placeholder="Введите вопрос"><br>

            <label class="awerds" for="points-${questionCount}">Баллы за вопрос:</label><br>
            <input class="number" type="number" id="points-${questionCount}" value="0" min="0"><br>
            <button type="button" class="add-btn" onclick="addAnswer(${questionCount})">Добавить Ответ</button><br>
            <div id="answers-${questionCount}" class="answer-container">
            <!-- Ответы будут добавляться сюда -->
            </div>
            <button type="button" class="add-btn" onclick="saveQuestionResult(); location.reload()">Добавить Вопрос</button><br>
            <div>
                <button class="add-btn" type="button" onclick="submitQuiz()">Отправить Квиз</button>
            </div>
        </div>

    `;

    questionContainer.innerHTML = questionHTML;
    document.getElementById('quiz-form').appendChild(questionContainer);
}

function addAnswer(questionId) {
    const answerContainer = document.createElement('div');
    const answerElements = document.querySelectorAll(`#answers-${questionId} div`);
    const answerCount = answerElements.length;

    const answerInputId = `answer-${questionId}-${answerCount}`;
    const answerLabelId = `answer-label-${questionId}-${answerCount}`;
    const correctId = `correct-${questionId}-${answerCount}`;

    answerContainer.innerHTML = `
        <div>
            <label class="textAns" for="${answerInputId}">Ответ ${((answerCount / 2) | 0) +1}:</label>
            <input class="answer" type="text" id="${answerInputId}" placeholder="Введите ответ">
            <label class="textLable">
                <input type="radio" name="correct-${questionId}" id="${correctId}"> Правильный
            </label>
        </div>
    `;

    document.getElementById(`answers-${questionId}`).appendChild(answerContainer);
}

function saveQuestionResult() {
    questions = JSON.parse(localStorage.getItem("Questions"));
    const questionText = document.getElementById(`question-${questionCount}`)?.value || '';
    const points = parseInt(document.getElementById(`points-${questionCount}`)?.value) || 0;

    const answers = [];
    const answerElements = document.querySelectorAll(`#answers-${questionCount} div`);

    answerElements.forEach((answerEl, index) => {
        const answerText = document.getElementById(`answer-${questionCount}-${index}`)?.value || '';
        const isCorrect = document.getElementById(`correct-${questionCount}-${index}`)?.checked || false;
        if (answerText!==""){
            answers.push({ text: answerText, correct: isCorrect });
        }
    });

    questions.push({
        question: questionText,
        points: points,
        answers: answers
    });
    localStorage.setItem("Questions", JSON.stringify(questions));
    localStorage.setItem("QuestionLength", JSON.stringify(questionCount))
}

function submitQuiz() {
    const quiz = JSON.parse(localStorage.getItem("Quiz"));
    questions = JSON.parse(localStorage.getItem("Questions"));
    const quizData = {
        title: quiz.title,
        description: quiz.description,
        questions: questions
    };
    try {
        const token = localStorage.getItem('authToken');
        console.log(JSON.stringify(quizData))
        fetch('quiz/add', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify(quizData)

        }).then(response => {
            if (response.ok){
                alert("Успех!!!!!!!")
                window.location.href = "/log";
            }
        });

    } catch (error) {
        console.error('Error:', error);
        alert('Ошибка валидации.');
    }
    localStorage.clear();
}