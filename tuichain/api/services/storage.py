from django.conf import settings
import dropbox


dbx = dropbox.Dropbox(settings.DBX_ACCESS_TOKEN)

dbx.users_get_current_account()


def upload_file(dbx, file, dest):
    print("TOU AQUI")
    metadata = dbx.files_upload(file, dest)
    print("DONE:", metadata)