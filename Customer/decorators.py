from django.http import HttpResponse
from django.shortcuts import redirect
from PIL import Image
import cv2
import os

# Get the static host from the environment variable if it exists.
STATIC_HOST = os.environ.get("DJANGO_STATIC_HOST", "")
if STATIC_HOST != "": 
    # If static host is not empty then append '/media/' to the static host.
    STATIC_HOST += "/media/"
else:
    # If static host is empty then append 'media/' to the static host.
    STATIC_HOST = "media/"


def unauthenticated_user(view_func):  # Decorator for unauthenticated users.
    """
    This decorator is used to restrict access to the view to unauthenticated users.
    .unauthenticated users: users who are not logged in.
    .view_func: view function to be decorated.
    """

    def wrapper_func(request, *args, **kwargs):
        """
        This function is used to check if the user is authenticated or not.
        .authenticated users: users who are logged in.
        *args: arguments passed to the view function.
        **kwargs: keyword arguments passed to the view function.
        """

        if request.user.is_authenticated:
            # If the user is authenticated, redirect to the home page.
            return redirect('Customer:dashboard')  # Redirect to the home page.
        else:
            # If the user is not authenticated, proceed to the view function.
            return view_func(request, *args, **kwargs)  # Proceed to the view function.

    return wrapper_func  # Return the wrapper function.


def allowed_users(allowed_roles=None):  # Decorator for allowed users.
    """
    This decorator is used to restrict access to the view to specific users.
    .allowed_roles: list of allowed roles.
    """

    if allowed_roles is None:
        # If the allowed_roles is None, then the decorator is used to restrict access to the view to all users.
        allowed_roles = []  # Initialize the allowed roles.

    def decorator(view_func):
        """
        This function is used to restrict access to the view to specific users.
        .view_func: view function to be decorated.
        """

        def wrapper_func(request, *args, **kwargs):
            """
            This function is used to check if the user is authenticated or not.
            .authenticated users: users who are logged in.
            *args: arguments passed to the view function.
            **kwargs: keyword arguments passed to the view function.
            .group: group of the user.
            """

            group = None  # Initialize the group.
            if request.user.groups.exists():  # Check if the user belongs to any group.
                # Get the very first group of the user and store it in the group variable.
                group = request.user.groups.all()[0].name

            if group in allowed_roles:  # Check if the group user belongs to the allowed roles.
                # If the group user belongs to the allowed roles, proceed to the view function.
                return view_func(request, *args, **kwargs)  # Proceed to the view function.
            else:
                # If the group user does not belong to the allowed roles,
                # give the user a message that he is not allowed to access the view.
                return HttpResponse('You are not authorized to view this page')

        return wrapper_func  # Return the wrapper function.

    return decorator  # Return the decorator.


def admin_only(view_func):  # Decorator for admin only.
    """
    This decorator is used to restrict access to the view to admin users.
    .view_func: view function to be decorated.
    """

    def wrapper_function(request, *args, **kwargs):
        """
        This function is used to check if the user belongs to admin group or not.
        .group: group of the user.
        *args: arguments passed to the view function.
        **kwargs: keyword arguments passed to the view function.
        """

        group = None  # Initialize the group.
        if request.user.groups.exists():  # Check if the user belongs to any group.
            # Get the very first group of the user and store it in the group variable.
            group = request.user.groups.all()[0].name

        if group == 'customer':  # Check if the group user belongs to the Customer group.
            # If the group user belongs to the Customer group, redirect to the same page on user was.
            return redirect('user-page')  # Redirect to the same page on user was.

        if group == 'admin':  # Check if the group user belongs to the Admin group.
            # If the group user belongs to the Admin group, proceed to the view function.
            return view_func(request, *args, **kwargs)  # Proceed to the view function.

    return wrapper_function  # Return the wrapper function.


def haveFaces(img):
    """
    ** Not a decorator **
    This function is used to check if the image contains a single human face or not,
    if it does then return True and the face coordinates.
    .img: image to be checked.
    """

    # Object of class CascadeClassifier is created.
    face_cascade = cv2.CascadeClassifier(os.path.join(cv2.data.haarcascades, 'haarcascade_frontalface_alt2.xml'))
    img = cv2.imread(STATIC_HOST + img)  # Read the image.
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Convert the image to grayscale.
    faces = face_cascade.detectMultiScale(gray, 1.3, 3)  # Detect the faces.

    if len(faces) == 1:  # Check if the image contains a single human face or not.
        cropper(img, faces[0])  # Crop the face.
        return True  # Return True and the face coordinates.
    else:
        return False, None  # Return False and None.


def cropper(img, cord):
    """
    ** Not a decorator **
    This function is used to crop the image.
    .img: image to be cropped.
    .cord: coordinates of the face in tuple format. (x, y, w, h)
    """

    x, y, w, h = cord  # Unpack the coordinates of the face.
    original_image = Image.open(STATIC_HOST + img)  # Open the image.
    cropped_img = original_image.crop((x, y, x + w, y + h))  # Crop the image.
    cropped_img.save(STATIC_HOST + img)  # Save the cropped image.

