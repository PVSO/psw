from datetime import datetime

from django.shortcuts import render, redirect

from django.contrib import messages
from django.contrib.messages import constants

from medico.models import DadosMedico, Especialidades, DatasAbertas, is_medico
from paciente.models import Consulta, Documento


def home(request):
    if request.method == 'GET':

        medicos = DadosMedico.objects.all()

        especialidades = Especialidades.objects.all()

        medico_filtrar = request.GET.get('medico')
        especialidades_filtrar = request.GET.getlist('especialidades')

        if medico_filtrar:
            medicos = medicos.filter(nome__icontains=medico_filtrar)

        if especialidades_filtrar:
            medicos = medicos.filter(especialidade_id__in=especialidades_filtrar)

        context = {
            'medicos': medicos,
            'especialidades': especialidades,
            'is_medico': is_medico(request.user)
        }

        return render(request,
                      'home.html',
                      context=context
                      )


def escolher_horario(request, id_dados_medicos):
    if request.method == "GET":
        medico = DadosMedico.objects.get(id=id_dados_medicos)
        datas_abertas = DatasAbertas.objects.filter(user=medico.user).filter(data__gte=datetime.now()).filter(agendado=False)

        context = {
            'medico': medico,
            'datas_abertas': datas_abertas,
            'is_medico': is_medico(request.user)
        }

        return render(request,
                      'escolher_horario.html',
                      context=context
                      )


def agendar_horario(request, id_data_aberta):
    if request.method == "GET":
        data_aberta = DatasAbertas.objects.get(id=id_data_aberta)

        horario_agendado = Consulta(
            paciente=request.user,
            data_aberta=data_aberta
        )

        horario_agendado.save()

        # TODO: Sugestão Tornar atomico

        data_aberta.agendado = True
        data_aberta.save()

        messages.add_message(request,
                             constants.SUCCESS,
                             'Consulta agendada com sucesso.'
                             )

        return redirect('/pacientes/minhas_consultas/')


def minhas_consultas(request):
    if request.method == "GET":
        #TODO: desenvolver filtros
        minhas_consultas = Consulta.objects.filter(paciente=request.user).filter(data_aberta__data__gte=datetime.now())

        context = {
            'minhas_consultas': minhas_consultas,
            'is_medico': is_medico(request.user)
        }
        return render(request, 'minhas_consultas.html', context=context)


def consulta(request, id_consulta):
    if request.method == 'GET':
        consulta = Consulta.objects.get(id=id_consulta)
        dado_medico = DadosMedico.objects.get(user=consulta.data_aberta.user)
        documento = Documento.objects.filter(consulta=consulta)

        context = {
            'consulta': consulta,
            'dado_medico': dado_medico,
            'documento': documento,
            'is_medico': is_medico(request.user)
        }

        return render(request, 'consulta.html', context=context)

# fazer validaçõa de segurança no restante do código
