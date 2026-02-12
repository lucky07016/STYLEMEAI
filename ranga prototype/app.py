from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import base64
from datetime import datetime

app = Flask(__name__)
# Allow requests from any origin (use stricter rules in production)
CORS(app)


def save_image_from_data_url(data_url: str) -> str | None:
    """Save a base64 data URL image to disk and return the file path."""
    if not data_url or not data_url.startswith("data:image"):
        return None

    try:
        header, encoded = data_url.split(",", 1)
        # default to png if we can't parse
        ext = "png"
        if "image/" in header:
            ext = header.split("image/")[1].split(";")[0] or "png"

        img_bytes = base64.b64decode(encoded)
        folder = "saved_photos"
        os.makedirs(folder, exist_ok=True)
        filename = datetime.now().strftime("%Y%m%d_%H%M%S_%f") + f".{ext}"
        path = os.path.join(folder, filename)
        with open(path, "wb") as f:
            f.write(img_bytes)
        return path
    except Exception:
        return None


def generate_suggestions(occasion: str, gender: str, style: str, budget: str):
    """
    Very simple rule-based suggestion generator.
    You can later replace this with a real AI model or API call.
    """
    occasion = (occasion or "").lower()
    gender = (gender or "").lower()
    style = (style or "").lower()
    budget = (budget or "").lower()

    # base suggestions from occasion (coarse recommendation)
    if occasion == "casual":
        suggestions = {
            "top": "Oversized cotton t-shirt or relaxed hoodie",
            "bottom": "Slim-fit jeans or joggers",
            "footwear": "Clean white sneakers",
            "colors": "Black • White • Grey • Denim blue",
            "tips": "Keep it simple and comfortable. Add a watch or cap for a bit of personality."
        }
    elif occasion == "college":
        suggestions = {
            "top": "Layered t-shirt with lightweight jacket or flannel",
            "bottom": "Straight-fit jeans or chinos",
            "footwear": "Sneakers or casual loafers",
            "colors": "Navy • Olive • Beige • White",
            "tips": "Prioritize comfort but add one statement piece like a patterned shirt or bold sneakers."
        }
    elif occasion == "party":
        suggestions = {
            "top": "Fitted shirt or stylish knit top",
            "bottom": "Black jeans or tailored trousers",
            "footwear": "Chelsea boots or sleek sneakers",
            "colors": "Black • Burgundy • Metallic accents",
            "tips": "Use texture (leather, satin, knit) and one standout accessory to look elevated without overdoing it."
        }
    elif occasion == "formal":
        suggestions = {
            "top": "Crisp button-down shirt or blouse, possibly with a blazer",
            "bottom": "Tailored trousers or a pencil skirt",
            "footwear": "Leather dress shoes or classic heels",
            "colors": "Navy • Charcoal • White • Soft pastels",
            "tips": "Make sure the fit is clean around shoulders and waist. Subtle accessories keep it professional."
        }
    else:
        # default / fallback suggestions
        suggestions = {
            "top": "Relaxed fit t-shirt or shirt",
            "bottom": "Dark blue jeans",
            "footwear": "Minimal sneakers",
            "colors": "Black • Navy • White",
            "tips": "Neutral tones keep your outfit clean and modern. Adjust layers based on weather."
        }

    # refine by gender / fit (silhouette & cuts)
    if gender == "female":
        suggestions["top"] = suggestions["top"].replace("t-shirt", "blouse or fitted top")
        suggestions["bottom"] = suggestions["bottom"].replace("jeans", "high-waisted jeans or skirt")
    elif gender == "male":
        suggestions["top"] = suggestions["top"].replace("shirt", "shirt or polo")
    elif gender == "neutral":
        suggestions["top"] = "Relaxed, gender-neutral top (boxy tee, sweatshirt, or shirt jacket)"
        suggestions["bottom"] = "Straight or wide-leg trousers/jeans with a comfortable fit"

    # refine by style (vibe of the outfit)
    if style == "minimal":
        suggestions["colors"] = "Black • White • Grey • Navy"
        suggestions["tips"] += " Keep silhouettes clean, avoid big logos, and stick to 2–3 colors."
    elif style == "streetwear":
        suggestions["top"] = "Graphic tee or oversized hoodie with a light jacket"
        suggestions["bottom"] = "Baggy jeans or cargos"
        suggestions["footwear"] = "Chunky sneakers or high-tops"
        suggestions["tips"] += " Play with layering, caps, and bold sneakers for a streetwear edge."
    elif style == "classic":
        suggestions["top"] = "Crisp shirt or knit with a simple jacket/blazer"
        suggestions["bottom"] = "Straight-fit chinos or well-fitted jeans"
        suggestions["footwear"] = "Loafers, derbies, or clean sneakers"
        suggestions["tips"] += " Focus on timeless pieces and avoid overly trendy details."
    elif style == "bold":
        suggestions["colors"] = "Jewel tones • Prints • Contrast color blocking"
        suggestions["tips"] += " Add one loud piece (print shirt, bright jacket, or statement shoes)."

    # refine by budget (where/how to shop)
    if budget == "low":
        suggestions["tips"] += " Look at high-street brands and thrift stores to recreate this affordably."
    elif budget == "medium":
        suggestions["tips"] += " Mix mid-range brands with a few quality basics that last longer."
    elif budget == "high":
        suggestions["tips"] += " Invest in premium fabrics and tailoring; focus on fit and material quality."

    return suggestions


@app.post("/suggest")
def suggest():
    data = request.get_json(silent=True) or {}
    occasion = data.get("occasion", "")
    gender = data.get("gender", "")
    style = data.get("style", "")
    budget = data.get("budget", "")
    image_data_url = data.get("image", "")

    saved_path = save_image_from_data_url(image_data_url)

    suggestions = generate_suggestions(occasion, gender, style, budget)

    if saved_path:
        suggestions["tips"] += " Your current look has been captured and saved for future styling sessions."

    return jsonify({
        "occasion": occasion or "any",
        "gender": gender or "any",
        "style": style or "any",
        "budget": budget or "any",
        "image_path": saved_path,
        **suggestions,
    })


if __name__ == "__main__":
    # Run the dev server
    app.run(host="127.0.0.1", port=5000, debug=True)


