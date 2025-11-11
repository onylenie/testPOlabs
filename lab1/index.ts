type Operation = (a: number, b?: number) => number;

// Чистые функции для математических операций
const add: Operation = (a, b = 0) => a + b;
const subtract: Operation = (a, b = 0) => a - b;
const multiply: Operation = (a, b = 1) => a * b;
const divide: Operation = (a, b = 1) => (b ? a / b : NaN);
const power: Operation = (a, b = 1) => Math.pow(a, b);
const sqrt: Operation = (a) => a > 0 ? Math.sqrt(a) : NaN;

// Состояние приложения как неизменяемый объект
interface CalculatorState {
    operandA: number;
    operandB: number | null;
    currentOperation: Operation | null;
}

const initialState: CalculatorState = {
    operandA: 0,
    operandB: null,
    currentOperation: null,
};

// Функция для изменения состояния
const updateState = (
    state: CalculatorState,
    update: Partial<CalculatorState>
): CalculatorState => {
    return { ...state, ...update };
};

// Состояние приложения. Вместо мутации мы будем использовать новую ссылку на объект.
let state: CalculatorState = { ...initialState };

// Функции управления (чистые)
const handleNumberClick = (value: string): void => {
    const resultInput = document.getElementById('result') as HTMLInputElement;
    resultInput.value += value;
};

// Функция для изменения знака текущего числа
const toggleSign = (): void => {
    const resultInput = document.getElementById('result') as HTMLInputElement;
    const currentValue = parseFloat(resultInput.value);

    if (isNaN(currentValue)) {
        // Если значение пустое или некорректное, ничего не делаем
        return;
    }

    // Изменяем знак числа и обновляем поле ввода
    resultInput.value = (-currentValue).toString();
};

// Функция для добавления десятичной точки
const handleDecimalClick = (): void => {
    const resultInput = document.getElementById('result') as HTMLInputElement;
    const currentValue = resultInput.value;

    // Проверяем, есть ли уже точка в текущем числе
    if (!currentValue.includes('.')) {
        resultInput.value += '.';
    }
};


const handleClick = (op: keyof typeof operations): void => {
    const resultInput = document.getElementById('result') as HTMLInputElement;
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
    } else if (state.currentOperation && state.operandB === null) {
        const result = state.currentOperation(state.operandA, currentValue);
        state = updateState(state, {
            operandA: result,
            currentOperation: null,
            operandB: null,
        });
        resultInput.value = result.toString();
    } else {
        state = updateState(state, {
            operandA: currentValue,
            currentOperation: operations[op],
            operandB: null,
        });
        resultInput.value = '';
    }
};

const calculate = (): void => {
    const resultInput = document.getElementById('result') as HTMLInputElement;
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

const clearResult = (): void => {
    const resultInput = document.getElementById('result') as HTMLInputElement;
    resultInput.value = '';
    state = { ...initialState }; // Создаем новый объект состояния (не мутируем)
};

// Объект с операциями (чистый, неизменяемый)
const operations: { [key: string]: Operation } = {
    '+': add,
    '-': subtract,
    '*': multiply,
    '/': divide,
    '^': power,
    'sqrt': sqrt,
};
