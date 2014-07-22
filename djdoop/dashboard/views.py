from django.conf import settings
from django.template import RequestContext, loader
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse_lazy
from django.views.decorators.csrf import csrf_exempt

from djdoop.core import *
from djdoop.core.views import get_data, put_data, is_member
#from djdoop.medical_history.forms import StudentForm as SmedForm

from djzbar.utils.informix import do_sql as do_esql

from djtools.decorators.auth import group_required
#from djtools.utils.date import calculate_age

@group_required('Staff')
def home(request):
    """
    main dashboard screen populated with a list of profiled pairs
    """
    pairs = None
    sql = '%s' % PROFILED_PAIRS
    objs = do_esql(sql)
    if objs:
        pairs = objs.fetchall()

    return render_to_response(
        "dashboard/home.html",
        {"pairs":pairs},
        context_instance=RequestContext(request)
    )

def get_students(request):
    """
    ajax POST returns a list of students
    """
    if request.POST:
        sql = '%s' % PROFILED_PAIRS
        objs = do_esql(sql)
        pairs = objs.fetchall()
        return render_to_response(
            "dashboard/profiled_pairs_data.inc.html",
            {"pairs":pairs,},
            context_instance=RequestContext(request)
        )
    else:
        return HttpResponse("error", mimetype="text/plain; charset=utf-8")

def panels(request,table,cid):
    """
    Takes database table and student ID.
    Returns the template data that paints the panels in the student detail view.
    """
    form = None
    obj = get_data(table,cid)
    if obj:
        data = obj.fetchone()
        if data:
            innit = {}
            if table == "cc_student_medical_history":
                for k,v in data.items():
                    innit[k] = v
                form = SmedForm(initial=innit)
            if table == "cc_athlete_medical_history":
                for k,v in data.items():
                    innit[k] = v
                form = AmedForm(initial=innit)
    t = loader.get_template("dashboard/panels/%s.html" % table)
    c = RequestContext(request, {'data':data,'form':form})
    return t.render(c)

@group_required('Medical Staff')
def student_detail(request,cid=None,template="dashboard/student_detail.html"):
    """
    main method for displaying student data
    """
    if not cid:
        # search form
        cid = request.POST.get("cid")
    if cid:
        # get student
        obj = do_esql("%s WHERE id_rec.id = '%s'" % (STUDENT_VITALS,cid))
        if obj:
            student = obj.fetchone()
            if student:
                try:
                    age = calculate_age(student.birth_date)
                except:
                    age = None
                ens = emergency_information(cid)
                shi = panels(request,"cc_student_health_insurance",cid)
                smh = panels(request,"cc_student_medical_history",cid)
                amh = panels(request,"cc_athlete_medical_history",cid)
            else:
                age=ens=shi=smh=amh=student=None
            return render_to_response(
                template,
                {
                    "student":student,"age":age,"ens":ens,
                    "shi":shi,"amh":amh,"smh":smh,"cid":cid
                },
                context_instance=RequestContext(request)
            )
        else:
            raise Http404
    else:
        raise Http404

@csrf_exempt
def xeditable(request):
    field = request.POST.get("name")
    value = request.POST.get("value")
    cid = request.POST.get("cid")
    table = request.POST.get("table")
    dic = {field:value}
    put_data( dic, table, cid )

    return HttpResponse(dic, mimetype="text/plain; charset=utf-8")
