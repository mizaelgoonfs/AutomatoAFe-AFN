# Conversor AFNe para AFN

Uma ferramenta que converte [Autômatos Finitos Não Determinísticos - com movimentos vazios (AFNe)](https://en.wikipedia.org/wiki/Nondeterministic_finite_automaton) para Autômatos Finitos Não Determinísticos (AFN) simples. O programa também faz o reconhecimento de palavras utilizando o AFNe de entrada.

Desenvolvido utilizando a linguagem Python.

## Guia para execução

1. Na pasta principal, insira seu arquivo de entrada no formato do seguinte exemplo:
    ~~~
    
    q2,q3,q4 //A primeira linha indica o conjunto de estados finais, separados por vírgula
    q0|a->q0|&->q1 //informa as transições de q0, seguindo a formatação
    q1|a->q1|b->q1|&->q2,q3 //informa as transições de q1
    q2|c->q2 //informa as transições de q2
    q3|a->q3|&->q4 //informa as transições de q3
    q4|b->q4 //informa as transições de q4
    
    ~~~

  *Observações:*

* O símbolo "&" representa uma transição vazia.
* Os comentários no arquivo de input devem ser ignorados, eles foram colocados somente com o intuito de explicar o que significa cada linha do input.
* O programa extrai o conjunto de estados e o alfabeto automaticamente
* A entrada sempre deve conter o estado q0, pois é assumido que este seja o estado inicial, ou seja, o estado definido na segunda linha do arquivo de entrada será o estado inicial.


2. Execute o programa com `python main.py`.

3. O programa pede que o usuário insira no teclado o nome do arquivo de entrada (incluindo a extensão).

4. O programa converte o AFNe e gera um arquivo de saída que representa o seu AFN equivalente.

5. O arquivo de saída `nomedoinput-AFN.txt`, é o resultado da conversão AFNe -> AFN.
    ~~~
    //Exemplo de arquivo de saída:
    
    q0 | a->[q0, q1, q2, q3, q4] | b->[q1, q2, q3, q4] | c->[q2]
    q1 | a->[q1, q2, q3, q4] | b->[q1, q2, q3, q4] | c->[q2]
    q2 | c->[q2]
    q3 | a->[q3, q4] | b->[q4]
    q4 | b->[q4]
    Conjunto de Estados Finais: [q0, q1, q2, q3, q4]
    
    ~~~
6. Após isso, o programa pede que o usuário digite a palavra a ser reconhecida pelo AFNe de entrada e informa se a palavra é ACEITA ou REJEITADA.
