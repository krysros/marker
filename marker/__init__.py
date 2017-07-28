from pyramid.config import Configurator
from pyramid.session import SignedCookieSessionFactory
import deform

from pkg_resources import resource_filename
from pyramid.i18n import get_localizer
from pyramid.threadlocal import get_current_request


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    with Configurator(settings=settings) as config:
        session_factory = SignedCookieSessionFactory(settings['session.secret'])
        config.set_session_factory(session_factory)
        config.include('.models')
        config.include('.routes')
        config.include('.security')
        deform.renderer.configure_zpt_renderer()

        config.add_translation_dirs(
            'colander:locale',
            'deform:locale',
        )

        def translator(term):
            return get_localizer(get_current_request()).translate(term)

        deform_template_dir = resource_filename('deform', 'templates/')
        zpt_renderer = deform.ZPTRendererFactory(
            [deform_template_dir],
            translator=translator)
        deform.Form.set_default_renderer(zpt_renderer)

        config.scan()
        return config.make_wsgi_app()
