from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
import google.generativeai as genai
from django.conf import settings
from .models import ChatMessage

# Configure Gemini API key
genai.configure(api_key=settings.GOOGLE_API_KEY)

@login_required(login_url='/login/')
def chatbot(request):
    # Fetch only current user's chat history
    chat_history = ChatMessage.objects.filter(user=request.user).order_by('timestamp')

    if request.method == "POST":
        # Handle Clear Chat
        if 'clear_chat' in request.POST:
            ChatMessage.objects.filter(user=request.user).delete()
            return redirect('chatbot')

        # Get text and image (both optional)
        user_input = request.POST.get("user_input", "").strip()
        uploaded_image = request.FILES.get("image_upload")

        if user_input or uploaded_image:
            # Save user's message/image
            msg = ChatMessage.objects.create(
                user=request.user,
                role="user",
                text=user_input,
                image=uploaded_image
            )

            # Generate AI response (text + image support)
            try:
                model = genai.GenerativeModel(
                    "gemini-2.5-flash",
                    safety_settings=[
                        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
                    ]
                )

                contents = []
                if user_input:
                    contents.append(user_input)
                if uploaded_image:
                    image_bytes = uploaded_image.read()
                    contents.append({
                        "mime_type": uploaded_image.content_type,
                        "data": image_bytes
                    })

                response = model.generate_content(contents)
                reply = response.text
            except Exception:
                reply = "Sorry, couldn't process the message/image. Try again!"

            # Save AI reply
            ChatMessage.objects.create(user=request.user, role="ai", text=reply)

            return redirect('chatbot')

    return render(request, "chat.html", {
        "chat_history": chat_history
    })

# Registration
def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('chatbot')
    else:
        form = UserCreationForm()
    return render(request, "register.html", {"form": form})

# Login
def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('chatbot')
    else:
        form = AuthenticationForm()
    return render(request, "login.html", {"form": form})