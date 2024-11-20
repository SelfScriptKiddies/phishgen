from phishgen import logger
import win32com.client, pythoncom

log = logger.get_logger(__name__)


def remove_document_properties(doc: win32com.client.CDispatch,
                               selected_properties: tuple[str] = ("Author", "Last Save By")) -> None:
    """
    Removes properties from a document

    :param doc: document object
    :param selected_properties: names of properties to remove
    """

    for properties in (doc.BuiltInDocumentProperties, doc.CustomDocumentProperties):
        for prop in properties:
            if prop.Name not in selected_properties:
                continue
            try:
                prop.Value = ""
            except Exception as e:
                log.error(f"Can't delete the property '{prop.Name}': {e}")

        try:
            doc.RemoveDocumentInformation(2)
        except Exception as e:
            log.error(f"Can't call remove document info: {e}")


def remove_comments_and_tracked_changes(doc):
    """
    Deletes all comments and tracked changes from a document

    :param doc: document object
    """
    try:
        comments = doc.Comments
        while comments.Count > 0:
            comments(1).Delete()
        log.debug("All comments were deleted")

        doc.ShowRevisions = False
        doc.TrackRevisions = False
        log.debug("Track revisions declined")
    except Exception as e:
        log.error(f"Error while deleting commends and tracked changes: {e}")
