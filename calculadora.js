// 1. Funções matemáticas isoladas
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
    let simbolo;

    if (isNaN(num1) || isNaN(num2)) {
        alert("Por favor, digite os dois números!");
        return;
    }

    switch (opcao) {
        case '1':
            resultado = somar(num1, num2);
            simbolo = '+';
            break;
        case '2':
            resultado = subtrair(num1, num2);
            simbolo = '-';
            break;
        case '3':
            resultado = multiplicar(num1, num2);
            simbolo = '*';
            break;
        case '4':
            resultado = dividir(num1, num2);
            simbolo = '/';
            break;
        default:
            resultado = "Operação inválida";
            simbolo = '?';
    }

    document.getElementById("resultado").innerText = resultado;

    // Adiciona ao Histórico
    let listaHistorico = document.getElementById("historico");
    let novoItem = document.createElement("li");
    novoItem.innerText = `${num1} ${simbolo} ${num2} = ${resultado}`;
    listaHistorico.appendChild(novoItem);
}