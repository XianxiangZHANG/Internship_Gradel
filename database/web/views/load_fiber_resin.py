from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from web import models


def get_fiber_data(request, fiber_id):
    fiber = get_object_or_404(models.Fiber, id=fiber_id)
    data = {
        'towInThousands': fiber.towInThousands,
        'tex': fiber.tex,
        'density': fiber.density,
    }
    return JsonResponse(data)

def get_resin_data(request, resin_id):
    resin = get_object_or_404(models.Resin, id=resin_id)
    data = {
        'hardener': resin.hardener,
        'curingCycle': resin.curingCycle,
        'densityR': resin.densityR,
    }
    return JsonResponse(data)
