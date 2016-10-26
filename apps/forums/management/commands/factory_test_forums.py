
import logging
import random

from utils.django.basecommands import FactoryCountBaseCommand

from ...factories import SectionFactory, ForumFactory, TopicFactory, PostFactory


logger = logging.getLogger('django.development')


class Command(FactoryCountBaseCommand):

    def handle(self, *args, **kwargs):

        count = kwargs['count'][0]

        SectionModel = SectionFactory._meta.model
        ForumModel = ForumFactory._meta.model
        TopicModel = TopicFactory._meta.model
        PostModel = PostFactory._meta.model

        SectionModel._default_manager.filter().delete()

        for i in range(count):
            section = SectionFactory()

            count_forums = random.randint(0, 5)

            for j in range(count_forums):
                forum = ForumFactory(section=section)

                count_topics = random.randint(0, 5)

                for k in range(count_topics):
                    topic = TopicFactory(forum=forum)

                    count_posts = random.randint(0, 5)

                    for l in range(count_posts):
                        PostFactory(topic=topic)

        logger.debug('Made factory {} sections, {} forums, {} topics, {} posts.'.format(
            SectionModel._default_manager.count(),
            ForumModel._default_manager.count(),
            TopicModel._default_manager.count(),
            PostModel._default_manager.count(),
        ))
