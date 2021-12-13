from django import template

register = template.Library()


@register.filter
def CalcCPUUse(CPUInDB):
    return round((CPUInDB / 100), 2)

@register.filter
def CalcUsingMemory(Memory):
    return Memory * 1024 * 1024
