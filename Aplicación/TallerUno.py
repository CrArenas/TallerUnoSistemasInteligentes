import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import requests
from io import BytesIO

# Recetas demo con etiquetas de salud
RECIPES = [
    {
        "name": "Ensalada Mediterránea",
        "image": "https://www.cocinatis.com/archivos/202305/CTIS0523-recetas-mediterraneas-que-te-haran-viajar.jpg",
        "ingredients": ["Tomates", "Pepino", "Aceitunas", "Queso feta", "Aceite de oliva"],
        "steps": "Cortar los vegetales, mezclar en un bowl y aliñar con aceite de oliva y queso feta.",
        "tags": ["diabetes", "hipertension"]
    },
    {
        "name": "Sopa de Lentejas",
        "image": "https://www.laylita.com/recetas/wp-content/uploads/2017/11/Sopa-de-lentejas.jpg",
        "ingredients": ["Lentejas", "Zanahoria", "Cebolla", "Apio", "Agua", "Sal baja en sodio"],
        "steps": "Hervir las lentejas, agregar vegetales picados y cocinar hasta ablandar.",
        "tags": ["diabetes"]
    },
    {
        "name": "Pollo a la plancha con verduras",
        "image": "https://www.recetasnestle.com.co/sites/default/files/styles/recipe_detail_desktop/public/srh_recipes/49e7d05602a1a7d4a1a2f1573e05fbc0.jpg",
        "ingredients": ["Pechuga de pollo", "Brócoli", "Zanahoria", "Aceite de oliva"],
        "steps": "Cocinar la pechuga a la plancha y saltear las verduras en aceite de oliva.",
        "tags": ["hipertension"]
    },
    {
        "name": "Fruta fresca con yogurt natural",
        "image": "https://t2.uc.ltmcdn.com/es/posts/4/1/9/como_hacer_yogur_con_frutas_naturales_47914_600.jpg",
        "ingredients": ["Frutas variadas", "Yogurt natural sin azúcar"],
        "steps": "Cortar frutas frescas y servir con yogurt natural sin azúcar.",
        "tags": ["diabetes", "hipertension"]
    },
    {
        "name": "Arroz blanco con zanahoria rallada",
        "image": "https://www.recetasnestle.com.pe/sites/default/files/styles/recipe_detail_desktop/public/2023-04/arroz-blanco.jpg",
        "ingredients": ["Arroz", "Agua", "Zanahoria rallada", "Un poco de sal"],
        "steps": "Hervir el arroz y añadir zanahoria rallada para darle suavidad y fibra.",
        "tags": ["gastroenteritis"]
    },
    {
        "name": "Puré de papa suave",
        "image": "https://www.paulinacocina.net/wp-content/uploads/2021/11/pure-de-papas-receta.jpg",
        "ingredients": ["Papas", "Leche descremada", "Un toque de mantequilla"],
        "steps": "Hervir las papas, hacer puré y añadir un poco de leche para suavizar.",
        "tags": ["gastroenteritis"]
    },
    {
        "name": "Sopa de avena con vegetales blandos",
        "image": "https://www.recetasnestle.com.ec/sites/default/files/styles/recipe_detail_desktop/public/srh_recipes/aa0b03f27d6d197f95d02ebea65dca77.jpg",
        "ingredients": ["Avena", "Zanahoria cocida", "Calabacín", "Agua"],
        "steps": "Cocinar avena en agua y añadir vegetales blandos para una sopa nutritiva.",
        "tags": ["demencia"]
    },
    {
        "name": "Batido de frutas con avena",
        "image": "https://www.recetasnestle.com.co/sites/default/files/styles/recipe_detail_desktop/public/receta-batido-de-avena-manzana.jpg",
        "ingredients": ["Banano", "Avena", "Leche descremada"],
        "steps": "Licuar todos los ingredientes hasta obtener una bebida cremosa y suave.",
        "tags": ["demencia"]
    }
]

class KitchenAssistantApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Asistente de Cocina - Saludable")
        self.root.geometry("1000x700")
        self.root.configure(bg="#f5f5f5")

        # --- Filtros ---
        filters_frame = tk.Frame(root, bg="#f5f5f5")
        filters_frame.pack(pady=10)

        self.filter_diabetes = tk.BooleanVar()
        self.filter_hipertension = tk.BooleanVar()
        self.filter_gastro = tk.BooleanVar()
        self.filter_demencia = tk.BooleanVar()

        tk.Label(filters_frame, text="Filtros de salud:", bg="#f5f5f5", font=("Arial", 12, "bold")).pack(side=tk.LEFT, padx=5)
        tk.Checkbutton(filters_frame, text="Diabetes", variable=self.filter_diabetes, bg="#f5f5f5").pack(side=tk.LEFT, padx=5)
        tk.Checkbutton(filters_frame, text="Hipertensión", variable=self.filter_hipertension, bg="#f5f5f5").pack(side=tk.LEFT, padx=5)
        tk.Checkbutton(filters_frame, text="Gastroenteritis", variable=self.filter_gastro, bg="#f5f5f5").pack(side=tk.LEFT, padx=5)
        tk.Checkbutton(filters_frame, text="Demencia", variable=self.filter_demencia, bg="#f5f5f5").pack(side=tk.LEFT, padx=5)

        tk.Button(filters_frame, text="Buscar Recetas", command=self.show_recipes, bg="#4CAF50", fg="white", font=("Arial", 12, "bold")).pack(side=tk.LEFT, padx=10)

        # --- Frame de recetas ---
        self.recipes_frame = tk.Frame(root, bg="#f5f5f5")
        self.recipes_frame.pack(fill="both", expand=True)

        # Scroll
        canvas = tk.Canvas(self.recipes_frame, bg="#f5f5f5")
        scrollbar = ttk.Scrollbar(self.recipes_frame, orient="vertical", command=canvas.yview)
        self.scrollable_frame = tk.Frame(canvas, bg="#f5f5f5")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def show_recipes(self):
        # Limpiar recetas anteriores
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        # Filtros seleccionados
        filters = []
        if self.filter_diabetes.get():
            filters.append("diabetes")
        if self.filter_hipertension.get():
            filters.append("hipertension")
        if self.filter_gastro.get():
            filters.append("gastroenteritis")
        if self.filter_demencia.get():
            filters.append("demencia")

        # Aplicar filtros
        filtered_recipes = []
        for recipe in RECIPES:
            if all(f in recipe["tags"] for f in filters):
                filtered_recipes.append(recipe)

        if not filtered_recipes:
            tk.Label(self.scrollable_frame, text="No se encontraron recetas con esos filtros.", bg="#f5f5f5", font=("Arial", 14, "italic"), fg="red").pack(pady=20)
            return

        # Mostrar recetas filtradas
        for recipe in filtered_recipes:
            frame = tk.Frame(self.scrollable_frame, bg="white", bd=2, relief="groove")
            frame.pack(padx=10, pady=10, fill="x")

            # Imagen más grande
            try:
                response = requests.get(recipe["image"])
                img = Image.open(BytesIO(response.content))
                img = img.resize((300, 200))
                photo = ImageTk.PhotoImage(img)
                img_label = tk.Label(frame, image=photo, bg="white")
                img_label.image = photo
                img_label.pack(side="left", padx=10, pady=10)
            except:
                tk.Label(frame, text="[Imagen no disponible]", bg="white").pack(side="left", padx=10, pady=10)

            # Info receta
            info_frame = tk.Frame(frame, bg="white")
            info_frame.pack(side="left", fill="both", expand=True, padx=10)

            tk.Label(info_frame, text=recipe["name"], font=("Arial", 16, "bold"), bg="white", fg="#333").pack(anchor="w")

            tk.Label(info_frame, text="Ingredientes:", font=("Arial", 12, "bold"), bg="white", fg="#444").pack(anchor="w")
            tk.Label(info_frame, text=", ".join(recipe["ingredients"]), font=("Arial", 12), bg="white", wraplength=600, justify="left").pack(anchor="w")

            tk.Label(info_frame, text="Preparación:", font=("Arial", 12, "bold"), bg="white", fg="#444").pack(anchor="w")
            tk.Label(info_frame, text=recipe["steps"], font=("Arial", 12), bg="white", wraplength=600, justify="left").pack(anchor="w")

if __name__ == "__main__":
    root = tk.Tk()
    app = KitchenAssistantApp(root)
    root.mainloop()
