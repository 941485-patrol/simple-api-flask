def stripper(form, field):
    field.data = str(field.data).strip()
    return field.data