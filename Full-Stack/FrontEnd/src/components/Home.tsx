import React, { useState, useEffect } from 'react';
import axios from 'axios';

function Home() {
    const [question, setQuestion] = useState('');
    const [answer, setAnswer] = useState('');
    const [userInput, setUserInput] = useState('');
    const [chatHistory, setChatHistory] = useState<{ role: string; content: any; }[]>([]);
    const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);

    useEffect(() => {
        axios.get(`/quiz?index=${currentQuestionIndex}`)
            .then(response => setQuestion(response.data.question));
    }, [currentQuestionIndex]);

    const handleChat = () => {
        axios.post('/chat', { user_input: userInput })
            .then(response => {
                setAnswer(response.data.answer);
                setChatHistory([...chatHistory, { role: "assistant", content: response.data.answer }]);
            });
    };

    const handleNextQuestion = () => {
        setCurrentQuestionIndex(currentQuestionIndex + 1);
    };

    return (
        <div>
            <h1>QuantumEd</h1>
            <p>Test your knowledge and learn more about quantum computing!</p>
            <p>{question}</p>
            <input type="text" value={userInput} onChange={e => setUserInput(e.target.value)} />
            <button onClick={handleChat}>Submit</button>
            <p>{answer}</p>
            <ul>
                {chatHistory.map((message, index) => (
                    <li key={index}>{message.content}</li>
                ))}
            </ul>
            <button onClick={handleNextQuestion}>Next Question</button>
        </div>
    );
}

export default Home;
