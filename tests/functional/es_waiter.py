import backoff
from elastic_transport import TransportError
from elasticsearch import Elasticsearch

from logger import get_logger
from settings import settings

logger = get_logger(__name__)


@backoff.on_exception(backoff.expo, (TransportError, AssertionError), logger=logger)
def wait_es():
    client = Elasticsearch(hosts=settings.es_url)
    assert client.ping()
    logger.info("connection with elasticsearch established")


if __name__ == "__main__":
    wait_es()
