# import base64
# import qrcode
# import onetimepass
# from io import BytesIO


# def get_secret(user):
#     return base64.b32encode(
#         (user.email + str(user.date_joined)).encode()
#     ).decode()


# def get_auth_url(email, secret, issuer='atom'):
#     url_template = 'otpauth://totp/{isr}:{uid}?secret={secret}&issuer={isr}'
#     return url_template.format(
#         uid=email,
#         secret=secret,
#         isr=issuer
#     )


# def get_image_b64(url):
#     qr = qrcode.make(url)
#     img = BytesIO()
#     qr.save(img)
#     return base64.b64encode(img.getvalue()).decode()


# def get_token(user):
#     return str(onetimepass.get_totp(get_secret(user)))
