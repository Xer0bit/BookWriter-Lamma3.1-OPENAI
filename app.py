from dotenv import load_dotenv
import os
from structure import get_structure
from events import get_events
from writing import write_book
from publishing import DocWriter
import random
from tqdm import tqdm
# Load environment variables from .env file
load_dotenv()

def generate_book():
    # Example input
    subject = "The History of the Internet"
    author_description = "A technology expert with a deep understanding of internet evolution"
    title = "The Internet's Journey: From ARPANET to the World Wide Web"


    chapters_input = """
    Chapter 1: The Early Days of Networking
    Chapter 2: The Birth of the Internet
    Chapter 3: The World Wide Web Revolution"""

    version = ''  # Choosing a version with 5000 to 10000 words

    # Define word count ranges based on version
    # version_limits = {
    #     '1': (15000, 20000),
    #     '2': (5000, 10000),
    #     '3': (2500, 5000)
    # }
    # min_words, max_words = version_limits.get(version, (None, None))
    # if min_words is None or max_words is None:
    #     raise ValueError('Invalid version selected.')

    # Define word count ranges based on version
    if version == '1':
        min_words, max_words = 15000, 20000
    elif version == '2':
        min_words, max_words = 5000, 10000
    elif version == '3':
        min_words, max_words = 2500, 5000
    else:
        return 'Invalid version selected.'
    # Process the input chapters
    chapter_dict = {}
    for chapter in chapters_input.splitlines():
        if ':' in chapter:
            key, value = chapter.split(':', 1)
            chapter_dict[key.strip()] = value.strip()

    total_chapters = len(chapter_dict)
    if total_chapters == 0:
        raise ValueError('Error: No chapters were provided. Please input at least one chapter.')

    # Calculate word count per chapter
    # total_word_count = random.randint(min_words, max_words)
    # words_per_chapter = total_word_count // total_chapters

    # Calculate word count per chapter
    average_word_count = (min_words + max_words) // 2
    words_per_chapter = average_word_count // total_chapters

    # Generate structure and events in a single pass
    title, plot, _ = get_structure(subject, 'non-fiction', author_description, title)
    # summaries_dict, event_dict = get_events(
    #     subject=subject,
    #     genre='non-fiction',
    #     author_description=author_description,
    #     profile='',
    #     title=title,
    #     plot=plot,
    #     chapter_dict=chapter_dict,
    #     # version=version
    #     words_per_chapter=words_per_chapter
    # )

    # Generate the book content in one step
    # book = write_book(
    #     subject=subject,
    #     genre='non-fiction',
    #     author_description=author_description,
    #     title=title,
    #     profile='',
    #     plot=plot,
    #     summaries_dict=summaries_dict,
    #     event_dict=event_dict,
    #     words_per_chapter=words_per_chapter
    # )
    # Set up progress bar for book generation
    progress_bar = tqdm(total=total_chapters, desc="Generating Book", unit="chapter")

    # Generate the book content directly
    book = write_book(
        subject=subject,
        genre='non-fiction',
        author_description=author_description,
        title=title,
        profile='',
        plot=plot,
        summaries_dict=None,  # No summaries needed
        event_dict={chapter: [title] for chapter in chapter_dict.keys()},  # Pass chapter titles directly
        words_per_chapter=words_per_chapter,
        progress_bar=progress_bar  # Pass progress bar to track progress
    )
    # Save the book
    doc_writer = DocWriter()
    doc_writer.write_doc(book, chapter_dict, title)

    print('Example book generated successfully! Check the docs folder for the output.')

if __name__ == '__main__':
    generate_book()

