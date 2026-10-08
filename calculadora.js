// 1. Funções matemáticas isoladas (O objetivo principal da refatoração)
function somar(a, b) { return a + b; }
function subtrair(a, b) { return a - b; }
function multiplicar(a, b) { return a * b; }
function dividir(a, b) {
    if (b === 0) return "Erro: Divisão por zero";
    return a / b;
}

// 2. Função acionada pelo botão do HTML
function calcular() {
    let num1 = parseFloat(document.getElementById("num1").value);
    let num2 = parseFloat(document.getElementById("num2").value);
    let opcao = document.getElementById("operacao").value;
    let resultado;

    // Validação simples
    if (isNaN(num1) || isNaN(num2)) {
        alert("Por favor, digite os dois números!");
        return;
    }

    // 3. O Switch-case que você pediu, apenas chamando as funções
    switch (opcao) {
        case '1':
            resultado = somar(num1, num2);
            break;
        case '2':
            resultado = subtrair(num1, num2);
            break;
        case '3':
            resultado = multiplicar(num1, num2);
            break;
        case '4':
            resultado = dividir(num1, num2);
            break;
        default:
            resultado = "Operação inválida";
    }

    // Exibe o resultado na tela
    document.getElementById("resultado").innerText = resultado;
}