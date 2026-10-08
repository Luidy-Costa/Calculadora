function executarCalculo(operacao, valor1, valor2) {
    let resultado;

    switch (operacao) {
        case 'soma':
            resultado = valor1 + valor2;
            console.log("O resultado da soma é: " + resultado);
            break;
        case 'subtracao':
            resultado = valor1 - valor2;
            console.log("O resultado da subtração é: " + resultado);
            break;
        case 'multiplicacao':
            resultado = valor1 * valor2;
            console.log("O resultado da multiplicação é: " + resultado);
            break;
        case 'divisao':
            if (valor2 === 0) {
                console.log("Erro: Não é possível dividir por zero!");
                resultado = null;
            } else {
                resultado = valor1 / valor2;
                console.log("O resultado da divisão é: " + resultado);
            }
            break;
        default:
            console.log("Operação inválida!");
            resultado = null;
    }

    return resultado;
}

// Executando alguns testes no código legado
executarCalculo('soma', 10, 5);
executarCalculo('divisao', 20, 2);