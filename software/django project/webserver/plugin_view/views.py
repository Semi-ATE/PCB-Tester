from django.http import FileResponse
from django.shortcuts import render
import pcbtesterinterface.viewinterface as interface
from pcbtesterinterface.viewinterface import dec_permissionrequired



@dec_permissionrequired("admin")
def download_excel(request):
    return FileResponse(interface.getPluginFileExcel(), as_attachment=True, filename='plugins.xlsx')

@dec_permissionrequired("admin")
def download_pdf(request):
    return FileResponse(interface.getPluginFilePdf(), as_attachment=True, filename='plugins.xlsx')

@dec_permissionrequired("runplugins")
def plugins(request):
    # task = startup.delay()
    ctx={
        'packagename': interface.getDetectedPlugin(),
        'versions': interface.getAvailableVersions(),
        'currentversion': interface.getCurrentVersion(),
        'pluginlist': interface.getAllDevicePluginNames(),
    }
    return render(request, 'plugin_view/plugins.html', ctx)

@dec_permissionrequired("admin")
def manageplugins(request):
    ctx={
        'plugins': interface.getPluginHistory()
    }
    return render(request, 'plugin_view/manageplugins.html', ctx)