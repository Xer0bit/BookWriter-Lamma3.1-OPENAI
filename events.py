from utils import BaseEventChain
import re
import random

# class ChapterPlotChain(BaseEventChain):
#     PROMPT = """
#     You are a writer, and your job is to generate content for one chapter of a non-fiction book.
#     The content for this chapter should be approximately {words_per_chapter} words.
#     Ensure the content is relevant, informative, and organized logically,
#     and matches the writing style of [Author Name].
#
#     Subject: {subject}
#     Genre: {genre}
#     Author: {author_description}
#
#     Title: {title}
#     Outline: {plot}
#
#     Chapter Plot:
#     {chapter}
#
#     # Return the content for that chapter:
#     Return the content for that chapter (limit to {words_per_chapter} words):"""
#
#     def run(self, subject, genre, author_description, profile, title, plot, chapter, words_per_chapter):
#         return self.chain.predict(
#             subject=subject,
#             genre=genre,
#             author_description=author_description,
#             profile=profile,
#             title=title,
#             plot=plot,
#             chapter=chapter,
#             words_per_chapter=words_per_chapter  # Pass words per chapter here
#         )

class ChapterPlotChain(BaseEventChain):
    PROMPT = """
    You are a writer, and your job is to generate content for one chapter of a non-fiction book.
    The content for this chapter should be approximately {words_per_chapter} words.
    Ensure the content is relevant, informative, and organized logically, 
    and matches the writing style of [Author Name].

    Subject: {subject}
    Genre: {genre}
    Author: {author_description}

    Title: {title}
    Outline: {plot}

    Chapter Plot:
    {chapter}

    Return the content for that chapter (limit to {words_per_chapter} words)::"""

    def trim_to_word_limit(self, text, word_limit):
        words = text.split()
        if len(words) > word_limit:
            text = ' '.join(words[:word_limit])
            # Ensure we end on a sentence boundary
            text = re.sub(r'\s+[^\s]*$', '', text).strip()
            if not text.endswith('.'):
                text += '.'
        return text

    def run(self, subject, genre, author_description, profile, title, plot, chapter, words_per_chapter):
        content = self.chain.predict(
            subject=subject,
            genre=genre,
            author_description=author_description,
            profile=profile,
            title=title,
            plot=plot,
            chapter=chapter,
            words_per_chapter=words_per_chapter
        )
        trimmed_content = self.trim_to_word_limit(content, words_per_chapter)
        return trimmed_content

class EventsChain(BaseEventChain):
    PROMPT = """
    You are a writer and your job is to outline the key points for the current chapter of a non-fiction book.
    These points should cover the main topics and subtopics that will be discussed in this chapter.
    Ensure the points are logical, relevant, and consistent with the overall outline.

    Subject: {subject}
    Genre: {genre}
    Author: {author_description}

    Title: {title}
    Outline: {plot}

    Key points for the current chapter:
    {summary}

    Return the key points:"""
    
    def run(self, subject, genre, author_description, profile, title, plot, summary, event_dict):
        previous_events = ''
        for chapter, events in event_dict.items():
            previous_events += '\n' + chapter
            for event in events:
                previous_events += '\n' + event

        response = self.chain.predict(
            subject=subject,
            genre=genre,
            author_description=author_description,
            profile=profile,
            title=title,
            plot=plot,
            summary=summary,
            previous_events=previous_events
        )
        return self.parse(response)
    
    def parse(self, response):
        point_list = response.strip().split('\n')
        point_list = [point.strip() for point in point_list if point.strip()]
        return point_list

# def generate_random_words(min_words, max_words):
#     return random.randint(min_words, max_words)
#
# def calculate_words_per_chapter(total_chapters, min_words, max_words):
#     total_words = generate_random_words(min_words, max_words)
#     return total_words // total_chapters
#
# def get_events(subject, genre, author_description, profile, title, plot, chapter_dict, version):
#     chapter_plot_chain = ChapterPlotChain()
#     events_chain = EventsChain()
#     summaries_dict = {}
#     event_dict = {}
#
#     # Define word count ranges based on version
#     if version == '1':
#         min_words, max_words = 15000, 20000
#     elif version == '2':
#         min_words, max_words = 5000, 10000
#     elif version == '3':
#         min_words, max_words = 2500, 5000
#     else:
#         raise ValueError('Invalid version selected.')
#
#     total_chapters = len(chapter_dict)
#     if total_chapters == 0:
#         raise ValueError('No chapters were provided. Please input at least one chapter.')
#
#     # Calculate words per chapter based on total chapters
#     words_per_chapter = calculate_words_per_chapter(total_chapters, min_words, max_words)
#
#     for chapter in chapter_dict:
#         summaries_dict[chapter] = chapter_plot_chain.run(
#             subject=subject,
#             genre=genre,
#             author_description=author_description,
#             profile=profile,
#             title=title,
#             plot=plot,
#             chapter=chapter,
#             words_per_chapter=words_per_chapter  # Pass the calculated words per chapter
#         )
#
#         event_dict[chapter] = events_chain.run(
#             subject=subject,
#             genre=genre,
#             author_description=author_description,
#             profile=profile,
#             title=title,
#             plot=plot,
#             summary=summaries_dict[chapter],
#             event_dict=event_dict
#         )
#
#     return summaries_dict, event_dict

def get_events(subject, genre, author_description, profile, title, plot, chapter_dict, words_per_chapter):
    chapter_plot_chain = ChapterPlotChain()
    events_chain = EventsChain()
    summaries_dict = {}
    event_dict = {}

    for chapter, _ in chapter_dict.items():
        summaries_dict[chapter] = chapter_plot_chain.run(
            subject=subject,
            genre=genre,
            author_description=author_description,
            profile=profile,
            title=title,
            plot=plot,
            chapter=chapter,
            words_per_chapter=words_per_chapter  # Pass the calculated words per chapter
        )

        event_dict[chapter] = events_chain.run(
            subject=subject,
            genre=genre,
            author_description=author_description,
            profile=profile,
            title=title,
            plot=plot,
            summary=summaries_dict[chapter],
            event_dict=event_dict
        )

    return summaries_dict, event_dict

