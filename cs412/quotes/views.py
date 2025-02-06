from django.shortcuts import render
import random

quotes = [
    "Hell was the journey but it brought me heaven.",
    "I'm damned if I do give a damn what people say.",
    "Spinning in my highest heels, love, shining just for you.",
    "And if you’re ever tired of being known for who you know, you know you’ll always know me.",
    "I'm so sick of them coming at me again, 'cause if I was the man, then I'd be the man."
]

images = [
    "taylor.jpg",
    "taylor1.jpg",
    "taylor2.jpg",
    "taylor3.jpg",
    "taylor4.jpg",
]  


def quote(request):
    """Randomly selects a quote and image """
    
    selected_quote = random.choice(quotes)
    selected_images = random.choice(images)
    
    request.session["selected_quote"] = selected_quote
    

    context = {
        "quote": selected_quote,
        "image": selected_images,  
        "name": "By Taylor Swift"
    }
    return render(request, "quotes/main.html", context)


def show_all(request):
    """Shows all Taylor Swift quotes with corresponding images."""

    
    paired_quotes_images = list(zip(quotes, images))  

    context = {
        "paired_quotes_images": paired_quotes_images  
    }
    return render(request, "quotes/show_all.html", context)


def about(request):
    """Displays biography of Taylor Swift and app creator details."""
    
    context = {
        "person_name": "Taylor Swift",
        "person_bio": " Taylor Alison Swift is a multi-Grammy award-winning American singer/songwriter who, in 2010 at the age of 20, became the youngest artist in history to win the Grammy Award for Album of the Year. In 2011 Swift was named Billboard's Woman of the Year. She also has been named the American Music Awards Artist of the Year, as well as the Entertainer of the Year for both the Country Music Association and the Academy of Country Music, among many other accolades. As of this writing, she is also the top-selling digital artist in music history. - IMDb",
        "creator_name": "Jess So",
        "creator_note": "Jess is one of the millions of the certified swifities across the world. She's been listening to Taylor's music ever since she was a little girl, and has found large inspiration from Taylor's beautifully-written lyrics and nostalgic voice. Some of her favorite songs from Taylor Swift's albums include The 1, Clean, Death by a Thousand Cuts, Love Story, and The Story of Us."
    }
    return render(request, "quotes/about.html", context)

