def stripData(form, field):
    if field.data is None:
        field.data=''
    field.data=str(field.data)
    field.data=field.data.strip()
    if form.id.data is None:
        form.id.data=''
    form.id.data=str(form.id.data)
    form.id.data=form.id.data.strip()
    return field.data, form.id.data