"use strict";
// Чистые функции для математических операций
const add = (a, b = 0) => a + b;
const subtract = (a, b = 0) => a - b;
const multiply = (a, b = 1) => a * b;
const divide = (a, b = 1) => (b ? a / b : NaN);
const power = (a, b = 1) => Math.pow(a, b);
const sqrt = (a) => a > 0 ? Math.sqrt(a) : NaN;
const initialState = {
    operandA: 0,
    operandB: null,
    currentOperation: null,
};
// Функция для изменения состояния
const updateState = (state, update) => {
    return Object.assign(Object.assign({}, state), update);
};
// Состояние приложения. Вместо мутации мы будем использовать новую ссылку на объект.
let state = Object.assign({}, initialState);
// Функции управления (чистые)
const handleNumberClick = (value) => {
    const resultInput = document.getElementById('result');
    resultInput.value += value;
};
// Функция для изменения знака текущего числа
const toggleSign = () => {
    const resultInput = document.getElementById('result');
    const currentValue = parseFloat(resultInput.value);
    if (isNaN(currentValue)) {
        // Если значение пустое или некорректное, ничего не делаем
        return;
    }
    // Изменяем знак числа и обновляем поле ввода
    resultInput.value = (-currentValue).toString();
};
// Функция для добавления десятичной точки
const handleDecimalClick = () => {
    const resultInput = document.getElementById('result');
    const currentValue = resultInput.value;
    // Проверяем, есть ли уже точка в текущем числе
    if (!currentValue.includes('.')) {
        resultInput.value += '.';
    }
};
const handleClick = (op) => {
    const resultInput = document.getElementById('result');
    const currentValue = parseFloat(resultInput.value);
    if (op === 'sqrt') {
        const operation = operations[op];
        const newResult = operation(currentValue);
        resultInput.value = newResult.toString();
        state = updateState(state, {
            operandA: newResult,
            currentOperation: null,
            operandB: null,
        });
    }
    else if (state.currentOperation && state.operandB === null) {
        const result = state.currentOperation(state.operandA, currentValue);
        state = updateState(state, {
            operandA: result,
            currentOperation: null,
            operandB: null,
        });
        resultInput.value = result.toString();
    }
    else {
        state = updateState(state, {
            operandA: currentValue,
            currentOperation: operations[op],
            operandB: null,
        });
        resultInput.value = '';
    }
};
const calculate = () => {
    const resultInput = document.getElementById('result');
    const currentValue = parseFloat(resultInput.value);
    if (state.currentOperation) {
        const result = state.currentOperation(state.operandA, currentValue);
        state = updateState(state, {
            operandA: result,
            currentOperation: null,
            operandB: null,
        });
        resultInput.value = result.toString();
    }
};
const clearResult = () => {
    const resultInput = document.getElementById('result');
    resultInput.value = '';
    state = Object.assign({}, initialState); // Создаем новый объект состояния (не мутируем)
};
// Объект с операциями (чистый, неизменяемый)
const operations = {
    '+': add,
    '-': subtract,
    '*': multiply,
    '/': divide,
    '^': power,
    'sqrt': sqrt,
};
