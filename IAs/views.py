import os
import pandas as pd
from .forms import *
from .models import *
from .resources import RemessaResources
from datetime import date, datetime
from django.contrib import messages
from django.views.generic import *
from tablib import Dataset
from django.http import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.
class Homepage(TemplateView):
    template_name = 'homepage.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('IAs:homefrotas')
        else:
            return super().get(request, *args, **kwargs)

class Criarconta(FormView):
    template_name = 'criarconta.html'
    form_class = CriarContaForm

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('IAs:login')

class Homefrotas(LoginRequiredMixin, ListView):
    template_name = 'homefrotas.html'
    model = Frota

class Detalhesfrotas(LoginRequiredMixin, DetailView):
    template_name = 'detalhefrotas.html'
    model = Frota

    @method_decorator(csrf_exempt, name='dispatch')
    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            frota = request.POST.get('frota_man')
            stts = Frota.objects.filter(numero = frota)
            print(frota, stts)
            stts.update(status = 'MANUTENÇÃO')

        return redirect('IAs:disponibilidade')

class Relatorios(LoginRequiredMixin, TemplateView):
    template_name = 'relatorios.html'

    @method_decorator(csrf_exempt, name='dispatch')
    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            data = request.POST.get('datahorariosaida')
            funcao = request.POST.get('funcao_down')
            status = request.POST.get('status_down')
            empresa = request.POST.get('empresa_down')

            if data != None:
                return download_horario_saida(request, data)
            elif funcao != None and status != None and empresa != None:
                return download_colaboradores(request, funcao, status, empresa)
            else:
                return download_disponibilidade(request)
        return redirect('IAs:homefrotas')

class Remessas(TemplateView):
    template_name = 'remessa.html'

def simple_upload(request):
    if request.method == 'POST':
        remessa_resources = RemessaResources()
        dataset = Dataset()
        new_remessa = request.FILES['myfile']

        if not new_remessa.name.endswith('xlsx'):
            messages.info(request,'wrong format')
            return redirect('IAs:homefrotas')
        import_data = dataset.load(new_remessa.read(), format='xlsx')
        for data in import_data:
            if data[0] == None or Remessa.objects.filter(remessa = str(data[0]).replace('AMPM.','')).exists():
                pass
                print(data[0], " - ", data[1], " - ",data[4], " - ", data[5], " - ", data[6], " - ", data[7])
            else:
                value = Remessa(Remessa.objects.count(),
                    str(data[0]).replace('AMPM.',''),
                    str(data[4]),
                    str(data[5]),
                    str(data[1]),
                    str(data[6]),
                    str(data[7]).split('.')[0]
                    )
                value.save()
    return render(request, 'remessa.html')
def disponibilidade(request):
    veiculos = Frota.objects.all()
    escalas = Escala.objects.filter(status='EM ENTREGA').all()
    manutencao = Frota.objects.filter(status = 'MANUTENÇÃO').all()

    if request.method == 'POST':

        status = request.POST.get('selectstatus1')

        if status == 'EM ROTA':
            pass
        else:
            frota = request.POST.get('selectfrotas1')
            remessa = request.POST.get('dispRemessa1')
            stts = Escala.objects.filter(remessa=remessa).all()
            stts.update(status='ENTREGUE')
            remessa = str(remessa).replace(' ','').split(';')

            for rem in remessa:
                remessas = Remessa.objects.filter(remessa=rem).all()
                remessas.update(status='ENTREGUE')

            motorista = request.POST.get('dispMotorista1')
            ajudante = request.POST.get('dispAjudante1')

            frotas = Frota.objects.filter(numero = frota)
            frotas.update(status=status)
            motoristas = Colaboradores.objects.filter(nome_guerra=motorista).all()
            motoristas.update(status='DISPONÍVEL')
            ajudantes = Colaboradores.objects.filter(nome_guerra = ajudante).all()
            ajudantes.update(status='DISPONÍVEL')
        return redirect('IAs:disponibilidade')

    return render(request, 'disponibilidade.html', {'escalas': escalas, 'veiculos': veiculos, 'manutencao': manutencao})

def escala(request):
    # Bancos que alimentam dados da página de escala
    periodos = Colaboradores.objects.all()
    listas = Frota.objects.filter(status = 'DISPONÍVEL', empresa = 'IPIRANGA').all()
    escalas = Escala.objects.order_by('-data').all()
    ajudantes = Colaboradores.objects.order_by('status1', 'tempo_s').reverse().filter(status = 'DISPONÍVEL').all()
    motoristas = Colaboradores.objects.order_by('status1', 'tempo_s').reverse().all()

    # Prazo de folgas, atestados, afastamentos e férias...

    # Paginação
    paginator = Paginator(escalas, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    remessas = Remessa.objects.filter(status = 'DISPONÍVEL')

    try:
        # Tratar período ausente baseado no dia da escala
        for i in periodos:
            if i.periodo == None or i.periodo == '':
                pass
            else:
                data = i.periodo
                data_tratada = datetime.strptime(str(data), "%Y-%m-%d").date()

                if data_tratada < date.today():
                    novo_periodo = Colaboradores.objects.filter(nome=i.nome)
                    novo_periodo.update(status='DISPONÍVEL', periodo=None)
    except:
        pass

    # Adicionar no banco de dados
    if request.method == 'POST':
        remessa = request.POST.get('remessa1')
        # Verificar se há encaixe
        if len(remessa) > 6:
            rem = str(remessa).split(';')
            for rem1 in rem:
                add = Remessa.objects.filter(remessa = rem1).all()
                add.update(status = 'EM ROTA')
        else:
            pass

        frota = request.POST.get('frota1')
        placa = request.POST.get('placa1')
        peso = request.POST.get('peso1')
        tipo = request.POST.get('tipo1')
        motorista = request.POST.get('motorista1')
        ajudante = request.POST.get('ajudante1')
        viagem = request.POST.get('viagem1')
        entregas = request.POST.get('entregas1')
        distancia = request.POST.get('distancia1')
        obs = request.POST.get('obs')

        escala = Escala(remessa = remessa, frota = frota, placa = placa, peso = peso, tipo_carga = tipo, motorista = motorista, ajudante = ajudante, viagem = viagem, entregas = entregas, distancia = distancia, observacao = obs)

        # Verificar se os campos abaixo estão vazios evitar um erro
        if frota == '' or placa == '' or peso == '' or ajudante == '' or motorista == '':
            pass
        else:

            # Mudança de status no Banco de Dados
            disp = Frota.objects.filter(numero = frota)
            disp.update(status = 'EM ROTA')

            mot = Colaboradores.objects.filter(nome_guerra = motorista)
            mot.update(status = 'EM ROTA')

            if ajudante == '-' or ajudante == 'CHAPA':
                pass
            else:
                aj = Colaboradores.objects.filter(nome_guerra = ajudante)
                aj.update(status = 'EM ROTA')

            rem = Remessa.objects.filter(remessa = remessa)
            rem.update(status ='EM ROTA')

            # Não deixar cadastrar duas vezes os mesmos dados
            if Escala.objects.filter(remessa = remessa).exists():
                pass
            else:
                escala.save()
            return redirect('IAs:escala')
    else:
        pass
    return render(request, 'escala.html', {'listas':listas, 'escalas':escalas, 'ajudantes': ajudantes, 'motoristas':motoristas, 'remessas': remessas, 'page_obj': page_obj})

def download_escala(request):
    try:
        if request.method == 'POST':
            data = request.POST.get('data1')

            queryset = Escala.objects.filter(data = data).all()

            # Crie um DataFrame com os dados do modelo
            df = pd.DataFrame(list(queryset.values()))

            df = df[['remessa','tipo_carga','frota','placa','motorista', 'viagem','ajudante']]
            df = df.rename(columns={'remessa':'REMESSA', 'tipo_carga': 'CATEGORIA', 'frota': 'FROTA', 'placa': 'PLACA', 'motorista': 'MOTORISTA', 'viagem': 'VIAGEM', 'ajudante': 'AJUDANTE' })

            # Defina o caminho e nome do arquivo Excel de saída
            # caminho = r"\Downloads"
            output_filename = f'\Escala-{data}.xlsx'

            # Exporte o DataFrame para um arquivo Excel
            df.to_excel(output_filename, index=False)

            # Abra o arquivo Excel para download
            with open(output_filename, 'rb') as file:
                response = HttpResponse(file.read(),'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                response['Content-Disposition'] = 'attachment; filename="{}"'.format(output_filename)
            return response
    except:
        return redirect('IAs:escala')
    return render(request, 'download_escala.html')

def download_disponibilidade(request):
    try:
        if request.method == 'POST':

            queryset = Frota.objects.filter(empresa = 'IPIRANGA').all()

            # Crie um DataFrame com os dados do modelo
            df = pd.DataFrame(list(queryset.values()))
            df = df[['numero', 'placa', 'tipo', 'bau', 'capacidade','status']]
            df['CARGA'] = 'CARRINHO'
            df = df.rename(columns={'numero': 'FROTA', 'placa': 'PLACA', 'tipo': 'TIPO', 'bau': 'BAÚ', 'capacidade': 'CAPACIDADE', 'status': 'STATUS' })

            # Defina o caminho e nome do arquivo Excel de saída
            output_filename = r'\Disponibilidade.xlsx'

            # Exporte o DataFrame para um arquivo Excel
            df.to_excel(output_filename, index=False)

            # Abra o arquivo Excel para download
            with open(output_filename, 'rb') as file:
                response = HttpResponse(file.read(),'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                response['Content-Disposition'] = 'attachment; filename="{}"'.format(output_filename)
            return response
    except:
        return redirect('IAs:escala')
    return render(request, 'relatorios.html')

def download_horario_saida(request, data):
    try:
        if request.method == 'POST':
            queryset = Escala.objects.filter(data = data).all()

            # Crie um DataFrame com os dados do modelo
            df = pd.DataFrame(list(queryset.values()))
            df = df[['remessa','frota', 'placa', 'tipo_carga', 'peso', 'motorista']]
            df['Entrega NF'] = ''
            df['Saída'] = ''
            df['Observação'] = ''

            df = df.rename(columns={'remessa':'Remessa', 'frota': 'Frota','placa': 'Placa', 'tipo_carga': 'Categoria', 'peso': 'Peso', 'motorista': 'Motorista'})

            # Defina o caminho e nome do arquivo Excel de saída

            output_filename = f'\Horário de Saída-{data}.xlsx'

            # Exporte o DataFrame para um arquivo Excel
            df.to_excel(output_filename, index=False)

            # Abra o arquivo Excel para download
            with open(output_filename, 'rb') as file:
                response = HttpResponse(file.read(), 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                response['Content-Disposition'] = 'attachment; filename="{}"'.format(output_filename)
            return response
    except:
        # return redirect('IAs:escala')

        messages.warning(request, "Data selecid")
    return render(request, 'relatorios.html')

def download_colaboradores(request, funcao, status, empresa):
    try:
        if request.method == 'POST':
            if funcao == 'TODOS' and status == 'TODOS' and empresa == 'TODOS':
                queryset = Colaboradores.objects.all()
            elif funcao == 'TODOS' and status != 'TODOS' and empresa != 'TODOS':
                queryset = Colaboradores.objects.filter(status=status, empresa=empresa).all()
            elif funcao == 'TODOS' and status == 'TODOS' and empresa != 'TODOS':
                queryset = Colaboradores.objects.filter(empresa=empresa).all()
            elif funcao != 'TODOS' and status != 'TODOS' and empresa == 'TODOS':
                queryset = Colaboradores.objects.filter(funcao=funcao, status=status).all()
            elif funcao != 'TODOS' and status == 'TODOS' and empresa != 'TODOS':
                queryset = Colaboradores.objects.filter(funcao=funcao, empresa=empresa).all()
            elif funcao != 'TODOS' and status == 'TODOS' and empresa == 'TODOS':
                queryset = Colaboradores.objects.filter(funcao=funcao).all()
            else:
                queryset = Colaboradores.objects.filter(status=status).all()

            # Crie um DataFrame com os dados do modelo
            df = pd.DataFrame(list(queryset.values()))

            # Defina o caminho e nome do arquivo Excel de saída
            output_filename =f'\Colaboradores.xlsx'

            # Exporte o DataFrame para um arquivo Excel
            df.to_excel(output_filename, index=False)

            # Abra o arquivo Excel para download
            with open(output_filename, 'rb') as file:
                response = HttpResponse(file.read(), 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                response['Content-Disposition'] = 'attachment; filename="{}"'.format(output_filename)
            return response
    except:
        return Colaboradores.objects.all()
    return render(request, 'relatorios.html')

def controle_func(request):
    folgas = Colaboradores.objects.filter(status='FOLGA', empresa='IPIRANGA').count()
    afastados = Colaboradores.objects.filter(status='AFASTADO', empresa='IPIRANGA').count()
    atestados = Colaboradores.objects.filter(status='ATESTADO', empresa='IPIRANGA').count()
    ferias = Colaboradores.objects.filter(status='FÉRIAS', empresa='IPIRANGA').count()
    disponiveis = Colaboradores.objects.filter(status='DISPONÍVEL', empresa='IPIRANGA').count()
    em_rota = Colaboradores.objects.filter(status='EM ROTA', empresa='IPIRANGA').count()

    funcionarios = Colaboradores.objects.order_by('nome').all()

    if request.method == 'POST':
        nome_cad = request.POST.get('nome_cad')
        nome_alt = request.POST.get('nome_alt')
        data_he = request.POST.get('data_he')
        arq_he = request.POST.get('arq_he')

        # Cadastro de dados
        if nome_cad != None:
            nome_guerra_cad = request.POST.get('nomeguerra_cad')
            funcao_cad = request.POST.get('funcao_cad')
            empresa_cad = request.POST.get('empresa_cad')

            nome_cad = str(nome_cad).upper()
            nome_guerra_cad = str(nome_guerra_cad).upper()

            if Colaboradores.objects.filter(nome = nome_cad).exists() or Colaboradores.objects.filter(nome_guerra = nome_guerra_cad).exists():
                pass
            else:
                colaboradores = Colaboradores(nome = nome_cad, nome_guerra = nome_guerra_cad, funcao = funcao_cad, status = 'DISPONÍVEL', horas = '00:00:00', status1= 'NULO', empresa = empresa_cad)
                colaboradores.save()
            return redirect('IAs:colaboradores')

        # Alteração de dados
        elif nome_alt != None:
            nome_guerra_alt = request.POST.get('nomeguerra_alt')
            funcao_alt = request.POST.get('funcao_alt')
            empresa_alt = request.POST.get('empresa_alt')
            status_alt = request.POST.get('status_alt')
            prazo_alt = request.POST.get('prazo_alt')
            if prazo_alt == None:
                prazo_alt = ''

            nome_alt = str(nome_alt).upper()
            nome_guerra_alt = str(nome_guerra_alt).upper()

            colaboradores = Colaboradores.objects.filter(nome_guerra = nome_guerra_alt)
            colaboradores.update(nome = nome_alt, nome_guerra = nome_guerra_alt, funcao = funcao_alt, status = status_alt, periodo = prazo_alt, empresa = empresa_alt)
            return redirect('IAs:colaboradores')
        else:
            horas_extras(request)

    return render(request, 'colaboradores.html', {'funcionarios': funcionarios,'folgas': folgas, 'atestados': atestados, 'afastados': afastados,'em_rota': em_rota, 'disponiveis': disponiveis,'ferias': ferias})

def horas_extras(request):
    # try:
        dataset = Dataset()
        new_remessa = request.FILES['arq_he']

        if not new_remessa.name.endswith('xlsx'):
            messages.info(request, 'wrong format')
            return redirect('IAs:homefrotas')

        import_data = dataset.load(new_remessa.read(), format='xlsx')
        for data in import_data:
            # print(data[3], data[7], data[8])
            if 'HORAS' in str(data[3]) or 'Nome de Guerra' in str(data[3]) or data[3] == None:
                pass
            else:
                hora = str(data[8])[:2]
                minuto = str(data[8])[3:5]
                hora_n = str(data[7])[:2]
                minuto_n = str(data[7])[3:5]
                if 'No' in hora:
                    if 'No' in hora_n:
                        pass
                    else:
                        segundos = int(hora_n) * 3600 + int(minuto_n) * 60
                        bd = Colaboradores.objects.filter(nome_guerra=str(data[3]))
                        bd.update(horas=str(data[7]), tempo_s='-' + str(segundos), status1='NEGATIVO')
                else:
                    segundos = int(hora) * 3600 + int(minuto) * 60
                    bd = Colaboradores.objects.filter(nome_guerra=str(data[3]))
                    bd.update(horas=str(data[8]), tempo_s=segundos, status1 = 'POSITIVO')

                if '00:00:00' in str(data[7]) and '00:00:00' in str(data[8]):
                    bd = Colaboradores.objects.filter(nome_guerra=str(data[3]))
                    bd.update(status1='NULO')
            # return redirect('IAs:colaboradores')
    # except:
    #     return redirect('IAs:homefrotas')
        return render(request, 'colaboradores.html')
