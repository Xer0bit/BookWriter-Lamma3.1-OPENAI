from utils import BaseStructureChain  # Removed ChatOpenAI import as it's no longer needed
import random

class TitleChain(BaseStructureChain):
    PROMPT = """
    Your job is to generate the title for a non-fiction book about the following subject. 
    Return a title and only a title!
    The title should be relevant to the subject matter.

    Subject: {subject}
    Genre: {genre}
    Author: {author_description}

    Title:"""

    def run(self, subject, genre, author_description):
        print(f"subject: {subject}, genre: {genre}, author_description: {author_description}")
        return self.chain.predict(
            subject=subject,
            genre=genre,
            author_description=author_description
        )

# Subject: {subject}
    # Title: {title}

class PlotChain(BaseStructureChain):
    PROMPT = """
    Your job is to regenerate the outline for a non-fiction book based on the given sequence. 
    Rewrite the existing chapters and headings into a coherent and logical structure.
    Return an outline.
    carefully see the number of chapters and headings and make sure they are in the right order.

    
    Genre: {genre}
    Author: {author_description}



    Outline:"""

    def run(self, subject, genre, author_description, title):
        return self.chain.predict(
            subject=subject,
            genre=genre,
            author_description=author_description,
            title=title
        )

# Headings range
def generate_random_number(min_val, max_val):
    return random.randint(min_val, max_val)

def get_structure(subject, genre, author_description, title):
    title_chain = TitleChain()
    plot_chain = PlotChain()

    # Generate title
    title = title_chain.run(subject, genre, author_description)

    # Generate plot
    plot = plot_chain.run(subject, genre, author_description, title)

    # Generate a random number of headings (between 3 and 7)
    num_headings = generate_random_number(3, 7)
    headings = [f"Heading {i + 1}" for i in range(num_headings)]

    return title, plot, headings
