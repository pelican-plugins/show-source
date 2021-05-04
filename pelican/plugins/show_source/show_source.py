import logging
import os
from urllib.parse import urljoin

from pelican import signals
from pelican.utils import pelican_open

logger = logging.getLogger(__name__)
source_files = []
TYPES_TO_PROCESS = ["articles", "pages", "drafts"]


def link_source_files(generator):
    """
    Processes each article/page object and formulates copy from and copy
    to destinations, as well as adding a source file URL as an attribute.
    """
    # Get all attributes from the generator that are articles or pages
    documents = sum(
        [
            getattr(generator, attr, None)
            for attr in TYPES_TO_PROCESS
            if getattr(generator, attr, None)
        ],
        [],
    )

    preserve_ext = generator.settings.get("SHOW_SOURCE_PRESERVE_EXTENSION", False)

    # Work on each item
    for post in documents:
        # condition to show a post
        if not (
            generator.settings.get("SHOW_SOURCE_ALL_POSTS")
            or post.metadata.get("show_source")
        ):
            logger.debug("show_source: sources not shown, aborting plugin")
            continue

        # Source file name can be optionally set in config
        show_source_filename = generator.settings.get(
            "SHOW_SOURCE_FILENAME", "{}.txt".format(post.slug)
        )
        try:
            # Get the full path to the original source file
            source_out = os.path.join(post.settings["OUTPUT_PATH"], post.save_as)

            # Get the path to the original source file
            source_out_path = os.path.split(source_out)[0]

            # Create 'copy to' destination for writing later
            copy_to = os.path.join(source_out_path, show_source_filename)

            # Add file to published path
            source_url = urljoin(post.save_as, show_source_filename)
        except Exception:
            logger.error(
                "show_source: Error processing source file for post", exc_info=True
            )

        # Preserve extension, if requested
        if preserve_ext:
            __, source_ext = os.path.splitext(post.source_path)

            copy_to_plain_name, __ = os.path.splitext(copy_to)
            copy_to = copy_to_plain_name + source_ext

            source_url_plain_name, __ = os.path.splitext(source_url)
            source_url = source_url_plain_name + source_ext

        # Format post source dict & populate
        out = {"copy_raw_from": post.source_path, "copy_raw_to": copy_to}

        logger.debug("Show Source: Will copy %s to %s", post.source_path, copy_to)
        source_files.append(out)
        # Also add the source path to the post as an attribute
        post.show_source_url = source_url


def _copy_from_to(from_file, to_file):
    """
    A very rough and ready copy from / to function.
    """
    with pelican_open(from_file) as text_in:
        encoding = "utf-8"
        with open(to_file, "w", encoding=encoding) as text_out:
            text_out.write(text_in)
            logger.info("show_source: Writing %s", to_file)


def write_source_files(*args, **kwargs):
    """
    Called by the `page_writer_finalized` signal to process source files.
    """
    for source in source_files:
        _copy_from_to(source["copy_raw_from"], source["copy_raw_to"])


def register():
    """
    Calls the shots, based on signals
    """
    signals.article_generator_finalized.connect(link_source_files)
    signals.page_generator_finalized.connect(link_source_files)
    signals.page_writer_finalized.connect(write_source_files)
