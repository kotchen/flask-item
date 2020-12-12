import os
import response

# i = 2

# path = os.getcwd() 
# image = open(path + '\\' + str(i) + '.jpg','rb')
# resp = Response(image, mimetype="i/jpeg")

# print(resp)

return send_file(
        io.BytesIO(imgByteArr),
        mimetype='image/png',
        as_attachment=True,
        attachment_filename='result.jpg'
    )