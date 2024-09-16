from utils import BaseEventChain
import re
from tqdm import tqdm
class WriterChain(BaseEventChain):
    PROMPT = """
    You are a non-fiction writer. The book is described by a list of key points.
    The content for this chapter should fit within the selected word count range of {words_per_chapter} words.
    Write in a style that matches [Author Name]’s tone and word choice.
    
    Your task is to ensure the content is concise and within the specified word limit.

    Genre: {genre}
    Author: {author_description}

    Title: {title}
    Subject: {subject}

    Outline:
    {plot}

    Previous points:
    {previous_events}

    Current Chapter summary: {summary}

    Previous paragraphs:
    {previous_paragraphs}

    Current key point:
    {current_event}

    Paragraphs of the book for that point:"""

    def run(self, subject, genre, author_description, title, profile, plot, previous_events, summary, previous_paragraphs, current_event, words_per_chapter):
        previous_events = '\n'.join(previous_events)
        generated_text = self.chain.predict(
            subject=subject,
            genre=genre,
            author_description=author_description,
            title=title,
            profile=profile,
            plot=plot,
            previous_events=previous_events,
            summary=summary,
            previous_paragraphs=previous_paragraphs,
            current_event=current_event,
            words_per_chapter=words_per_chapter  # Pass words per chapter here
        )
        
        # Calculate the actual word count
        word_count = len(re.findall(r'\w+', generated_text))
        
        # Trim or expand content if necessary
        if word_count > words_per_chapter:
            words = generated_text.split()
            generated_text = ' '.join(words[:words_per_chapter])
        elif word_count < words_per_chapter:
            additional_text = self.chain.predict(
                subject=subject,
                genre=genre,
                author_description=author_description,
                title=title,
                profile=profile,
                plot=plot,
                previous_events=previous_events,
                summary=summary,
                previous_paragraphs=generated_text,
                current_event=current_event,
                words_per_chapter=words_per_chapter - word_count  # Generate remaining words
            )
            generated_text += ' ' + additional_text
        
        return generated_text

# def write_book(subject, genre, author_description, title, profile, plot, summaries_dict, event_dict, words_per_chapter):
#     writer_chain = WriterChain()
#     previous_events = []
#     book = {}
#     paragraphs = ''
#
#     for chapter, event_list in event_dict.items():
#         book[chapter] = []
#
#         for event in event_list:
#             paragraphs = writer_chain.run(
#                 subject=subject,
#                 genre=genre,
#                 author_description=author_description,
#                 title=title,
#                 profile=profile,
#                 plot=plot,
#                 previous_events=previous_events,
#                 summary=summaries_dict[chapter],
#                 previous_paragraphs=paragraphs,
#                 current_event=event,
#                 words_per_chapter=words_per_chapter  # Pass words per chapter here
#             )
#
#             previous_events.append(event)
#             book[chapter].append(paragraphs)
#
#     return book


def write_book(subject, genre, author_description, title, profile, plot, summaries_dict, event_dict, words_per_chapter,
               progress_bar=None):
    writer_chain = WriterChain()
    previous_events = []
    book = {}
    paragraphs = ''

    total_events = sum(len(event_list) for event_list in event_dict.values())

    # Initialize the progress bar if it's not passed in
    if progress_bar is None:
        progress_bar = tqdm(total=total_events, desc="Writing Book", unit="event")

    for chapter, event_list in event_dict.items():
        book[chapter] = []

        for event in event_list:
            paragraphs = writer_chain.run(
                subject=subject,
                genre=genre,
                author_description=author_description,
                title=title,
                profile=profile,
                plot=plot,
                previous_events=previous_events,
                summary=summaries_dict[chapter],
                previous_paragraphs=paragraphs,
                current_event=event,
                words_per_chapter=words_per_chapter
            )

            previous_events.append(event)
            book[chapter].append(paragraphs)

            # Update the progress bar
            progress_bar.update(1)

    return book