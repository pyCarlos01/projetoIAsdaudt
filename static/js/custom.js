function novaRemessa(dados) {
    document.getElementById('dialog_remessa').showModal();
}

// Dialog remessas
function remessaEncaixe(dados) {
// Limpar a lista
    document.getElementById('dialog_remessas').showModal();
    const li = document.getElementById('ulremessas1');
    console.log(li);
    li.innerHTML = '';
    console.log('carlos');
    remessas.forEach(rem =>{
        if('DISPONÍVEL' == rem.status){
            var li = document.createElement('li');
            var button = document.createElement('input');
            button.type = 'button';
            button.value = rem.remessa;
            check = document.getElementById('check')

            button.addEventListener("click", function() {
                if(check.checked == true){
                    var encaixe = document.getElementById('remessa' + dados);
                    var kg = document.getElementById('peso' + dados);
                    var valorAntigo = encaixe.value;
                    var valorNovo = button.value;
                    var pesoAntigo = parseInt(kg.value);
                    var pesoNovo = parseInt(rem.peso);

                    encaixe.value = valorAntigo + ';' + valorNovo;
                    kg.value = pesoAntigo + pesoNovo
                    verificarPeso(kg.value)
                    document.getElementById('limpar1').style.display = 'block'
                    document.getElementById('dialog_remessas').close();
                }
                else{
                    document.getElementById('remessa' + dados).value = button.value
                    document.getElementById('limpar1').style.display = 'block'
                    peso(1)
                    document.getElementById('dialog_remessas').close();
                };
            });
                li.appendChild(button);

                var ul = document.getElementById('ulremessas' + dados);
                ul.appendChild(li);

        }
    })
}

function verificarPeso(peso){
    info.forEach(frota=>{
        var frotas = document.getElementById('frota1').value;
        if(frotas == frota.frota){
            if(peso < frota.peso){
                console.log(frota.frota, frota.peso, peso)
            }

            else{
                document.getElementById('dialog_remessas').close();
                carregarFrotas(1)
            };
        };
    })
}

function carregarFrotas(dados){
    document.getElementById('dialog_frotas').showModal();
    var peso = document.querySelector('#peso' + dados);
    var valorPeso = peso.value;
    const li = document.getElementById('ulfrotas1');
    li.innerHTML = '';

    const lista = document.querySelector('#ulfrotas' + dados);
    info.forEach(frota => {
        if ('DISPONÍVEL' == frota.status && valorPeso <= frota.peso){
            var li = document.createElement('li');
            var button = document.createElement('input');
            button.type = 'button';
            button.value = frota.frota;


            button.addEventListener("click", function() {
            document.getElementById('frota1').value = button.value
            pesquisarFrotas(1)
            document.getElementById('dialog_frotas').close();
            });

            li.appendChild(button);

            var ul = document.getElementById("ulfrotas1");
            ul.appendChild(li);
        };
    })}

function peso(dados){
    var r = document.querySelector('#remessa' + dados);
    var valorRemessa = r.value;

    document.getElementById('frota' + dados).value = ""
    document.getElementById('placa' + dados).value = ""
    document.getElementById('motorista' + dados).value = ""
    document.getElementById('ajudante' + dados).value = ""
    document.getElementById('tipo' + dados).value = ""

    remessas.forEach(rem => {
        if(valorRemessa == rem.remessa){
            document.getElementById('peso'+ dados).value = rem.peso
            document.getElementById('placa' + dados).value = rem.placa
            document.getElementById('tipo' + dados).value = rem.categoria
            document.getElementById('entregas' + dados).value = rem.entregas
            document.getElementById('distancia' + dados).value = rem.distancia
            pesquisar(1)
    };
    })}

function dispFrota(dados) {
    document.getElementById('dialog_disp').showModal();
}

function fechar(dados) {
        const li = document.getElementById('ulclasses' + dados);
        li.innerHTML = "";
        document.getElementById('disp_classes1').close();
}

function fechar2(dados) {
        const li = document.getElementById('ulmotorista');
        li.innerHTML = "";
        document.getElementById('dialog_novoMotorista1').close();
}


function dispClasse(dados, tipo) {
    document.getElementById('disp_classes1').showModal();
    document.getElementById('desc_classes' + dados).innerText = 'Veículos filtrados, referentes a classe ' + tipo

    let text = tipo.charAt(0).toUpperCase() + tipo.slice(1).toLowerCase();

    img = document.querySelector('#imgclasses' + dados);
    img.src = '/static/image/' + text + '.jpg'

    info.forEach(frotas => {
        if(tipo == frotas.tipo){
            var li = document.createElement('li');
            var label = document.createElement('label')
            var button = document.createElement('input');
            button.type = 'submit';
            button.value = frotas.frota + ' ';
            label.innerText = ' - ' + frotas.tipo + ' - ' + frotas.status;

            button.addEventListener('click', function(){
                document.getElementById('Formclasses1').action = frotas.id;
            });

            li.appendChild(button);
            li.appendChild(label);

            var ul = document.getElementById('ulclasses1');
            ul.appendChild(li);
        };
    })}

function fecharRemessa(dados) {
    document.getElementById('remessa' + dados).value = ""
    document.getElementById('frota' + dados).value = ""
    document.getElementById('placa' + dados).value = ""
    document.getElementById('motorista' + dados).value = ""
    document.getElementById('ajudante' + dados).value = ""
    document.getElementById('peso' + dados).value = ""
    document.getElementById('tipo' + dados).value = ""
    document.getElementById('dialog_remessa').close();
}

function fecharFrota(dados) {
    document.getElementById('selectfrotas' + dados).value = ""
    document.getElementById('dispRemessa' + dados).value = ""
    document.getElementById('dispMotorista' + dados).value = ""
    document.getElementById('dispAjudante' + dados).value = ""
    document.getElementById('dialog_disp').close();
}

function novoMotorista(dados) {
    document.getElementById('dialog_novoMotorista1').showModal();
    const li = document.getElementById('ulmotorista');
    li.innerHTML = '';
    var frota = document.getElementById('frota1');
    var valorFrota = frota.value;
    const lista = document.getElementById('ulmotorista')
    info.forEach(frotas => {
        if(valorFrota == frotas.frota){
            var valorTipo = frotas.tipo
            if('VUC' == valorTipo){
                funcao.forEach(funcoes =>{
                    if('DISPONÍVEL' == funcoes.status){
                        if('MOTORISTA VUC' == funcoes.funcao || 'MOTORISTA MÉDIO' == funcoes.funcao || 'MOTORISTA PESADO' == funcoes.funcao){
                            var li = document.createElement('li');
                            var button = document.createElement('input');
                            button.type = 'button';
                            button.value = funcoes.motorista;

                            button.addEventListener('click', function(){
                                document.getElementById('motorista1').value = button.value
                                document.getElementById('dialog_novoMotorista1').close();
                            });

                            li.appendChild(button);


                            var ul = document.getElementById("ulmotorista");
                            ul.appendChild(li);
                        }
                    }
                })
            }
            else if('MEDIO' == valorTipo || 'TOCO' == valorTipo || 'TRUCK' == valorTipo ){
                funcao.forEach(funcoes =>{
                    if('Disponível' == funcoes.status){
                        if('MOTORISTA MÉDIO' == funcoes.funcao || 'MOTORISTA PESADO' == funcoes.funcao){
                            var li = document.createElement('li');
                            var button = document.createElement('input');
                            button.type = 'button';
                            button.value = funcoes.motorista;

                            button.addEventListener('click', function(){
                                document.getElementById('motorista1').value = button.value
                                document.getElementById('dialog_novoMotorista1').close();
                            });

                            li.appendChild(button);


                            var ul = document.getElementById("ulmotorista");
                            ul.appendChild(li);
                        }
                    }
                })
            }
            else if('CARRETA' == valorTipo){
                funcao.forEach(funcoes =>{
                    if('DISPONÍVEL' == funcoes.status){
                        if('MOTORISTA PESADO' == funcoes.funcao){
                            var li = document.createElement('li');
                            var button = document.createElement('input');
                            button.type = 'button';
                            button.value = funcoes.motorista;

                            button.addEventListener('click', function(){
                                document.getElementById('motorista1').value = button.value
                                document.getElementById('dialog_novoMotorista1').close();
                            });

                            li.appendChild(button);


                            var ul = document.getElementById("ulmotorista");
                            ul.appendChild(li);
                        }
                    }
                })
            };
        };
    })
}


function pesquisar(registro){
    document.getElementById('motorista1').value = ""
    var placa = document.querySelector('#placa' + registro);
    var valorPlaca = placa.value;
    info.forEach(caract => {
        if(valorPlaca == caract.placa){
            document.getElementById('frota'+ registro).value = caract.frota
            var valorMotorista = caract.motorista;
            funcao.forEach(status => {
                if(valorMotorista == status.motorista){
                    if('DISPONÍVEL' == status.status && valorMotorista != '-'){
                        document.getElementById('motorista1').value = status.motorista
                    }
                    else{
                        novoMotorista(1)
                    };
                };
            })



        };
    })}

function pesquisarFrotas(registro){
    document.getElementById('motorista1').value = ""
    var frota = document.querySelector('#frota' + registro);
    var valorFrota = frota.value;
    info.forEach(caract => {
        if(valorFrota == caract.frota){
            document.getElementById('placa'+ registro).value = caract.placa
            var valorMotorista = caract.motorista;
            funcao.forEach(status => {
                if(valorMotorista == status.motorista){
                    if('DISPONÍVEL' == status.status){
                        document.getElementById('motorista1').value = status.motorista
                    }
                    else{
                        novoMotorista(1)
                    };
                };
            })
        };
    })}

function limparEncaixe(dados){
    document.getElementById('remessa' + dados).value = ""
    document.getElementById('frota' + dados).value = ""
    document.getElementById('placa' + dados).value = ""
    document.getElementById('motorista' + dados).value = ""
    document.getElementById('ajudante' + dados).value = ""
    document.getElementById('peso' + dados).value = ""
    document.getElementById('tipo' + dados).value = ""
    document.getElementById('limpar1').style.display = 'none'
}

function disp(dados){
    var f = document.querySelector('#selectfrotas' + dados);
    var valorFrota = f.value;
    esc.forEach(escala => {
        if(valorFrota == escala.frota){
            document.getElementById('dispRemessa' + dados).value = escala.remessa
            document.getElementById('dispMotorista' + dados). value = escala.motorista
            document.getElementById('dispAjudante' + dados). value = escala.ajudante
        };
    })

}

function carregarDisp(){
    document.getElementById('dialog_stts').showModal();

    const li = document.getElementById('ulstts');
    li.innerHTML = '';

    const lista = document.querySelector('#ulstts');
    esc.forEach(frota => {
        var li = document.createElement('li');
        var button = document.createElement('input');
        var label = document.createElement('label');
        button.type = 'button';
        button.value = frota.frota;
        label.innerText = ' - ' + frota.status;

        button.addEventListener("click", function() {
        document.getElementById('selectfrotas1').value = button.value
        disp(1)
        document.getElementById('dialog_stts').close();
        });
        li.appendChild(button);
        li.appendChild(label);


        var ul = document.getElementById("ulstts");
        ul.appendChild(li);
    })}

function alterarColaborador(){
    var col = document.querySelector('#nome_alt');
    var valorCol = col.value;

    colaboradores.forEach(colaborador =>{
        if(colaborador.nome == valorCol){
            document.getElementById('nomeguerra_alt').value = colaborador.nome_guerra;
            document.getElementById('funcao_alt').value = colaborador.funcao;
            document.getElementById('empresa_alt').value = colaborador.empresa;
            document.getElementById('status_alt').value = colaborador.status;
        }
        else if(valorCol == ''){
            document.getElementById('nomeguerra_alt').value = "";
            document.getElementById('funcao_alt').value = "";
            document.getElementById('empresa_alt').value = "";
            document.getElementById('status_alt').value = "";
        };
    })
}

function definirPrazo(){
    var status = document.querySelector('#status_alt');
    var valorStatus = status.value;
    if(valorStatus == 'FÉRIAS' || valorStatus == 'ATESTADO' || valorStatus == 'AFASTADO' || valorStatus == 'FOLGA'){
        document.getElementById('prazo_alt').value = ''
        document.getElementById('label_alt').style.display = 'block'
        document.getElementById('prazo_alt').style.display = 'block'
        document.getElementById('prazo_alt').required = true
    }
    else{
        document.getElementById('label_alt').style.display = 'none'
        document.getElementById('prazo_alt').style.display = 'none'
        document.getElementById('prazo_alt').value = ''
        document.getElementById('prazo_alt').required = false

    };
}

function edt(d, f, p, r, m, k, a, v, t, e, l, o){
    document.getElementById('data_edt').value = d
    document.getElementById('frota_edt').value = f
    document.getElementById('placa_edt').value = p
    document.getElementById('remessa_edt').value = r
    document.getElementById('motorista_edt').value = m
    document.getElementById('peso_edt').value = k
    document.getElementById('ajudante_edt').value = a
    document.getElementById('viagem_edt').value = v
    document.getElementById('categoria_edt').value = t
    document.getElementById('entregas_edt').value = e
    document.getElementById('distancia_edt').value = l

    if(o == 'None'){
        document.getElementById('obs_edt').value = ''
    }
    else{
        document.getElementById('obs_edt').value = o
    };

}

//function limpar_H(){
//    document.getElementById('datahorariosaida').value = ""
//}
//
//function limpar_E(){
//    document.getElementById('data1').value = ""
//}
//
//function limpar_C(){
//    document.getElementById('funcao_down').value = ""
//    document.getElementById('status_down').value = ""
//    document.getElementById('empresa_down').value = ""
//}
