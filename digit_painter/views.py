from django.shortcuts import render, redirect
import base64
import numpy as np
import re
import PIL.Image
import io
import digit_painter.cnn as cnn


def paint(request):
    return render(request, "digit_painter/paint.html")


def submit(request):
    # Strip the beginning metadata
    try:
        img_base64 = re.search(r"base64,(.*)", request.POST["img_base64"]).group(1)
    except AttributeError:
        return redirect("/")

    # Converting the string requires a round-about way:
    #   First, a conversion to a bytestring
    #   Second, storage in a BytesIO mock file object
    #   Third, loading it as an image and resize the image to 28 x 28 pixels
    #   Fourth, converting it to a numpy array
    #   Fifth, select only the last slice of the 3D cube as this will always be a grayscale image
    # I'm super unhappy about this but couldn't find a cleaner method
    base64_string = base64.b64decode(img_base64)
    bytes_object = io.BytesIO(base64_string)
    image_object = PIL.Image.open(bytes_object).resize((28, 28), PIL.Image.NEAREST)
    img = np.array(image_object)[..., -1]

    # Normalize
    # img[img > 0] = 1

    # Send numpy array into neural network and obtain results
    result, prob = cnn.classify_image(img)

    # Convert the NumPy array into an image and convert to base64 again
    arr_img = PIL.Image.fromarray((255 - img), mode="L").resize((280, 280), resample=PIL.Image.NEAREST)
    buffer = io.BytesIO()
    arr_img.save(buffer, format="PNG")
    arr_img_base64 = 'data:image/png;base64,' + base64.b64encode(buffer.getvalue()).decode("utf-8")

    return render(request, "digit_painter/results.html", {
        "img": arr_img_base64, "result": result, "prob": "{:.2f}".format(prob * 100)})
