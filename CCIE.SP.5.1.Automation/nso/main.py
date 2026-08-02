# -*- mode: python; python-indent: 4 -*-
import ncs
from ncs.application import Service


class ServiceCallbacks(Service):

    @Service.create
    def cb_create(self, tctx, root, service, proplist):
        self.log.info('Service create(service=', service._path, ')')

        # Guard-rail example: refuse .0 host part (why not - it is our workbook,
        # our rules). This is where per-service validation/logic lives.
        if service.ipv4_address.endswith('.0'):
            raise Exception('Loopback address must not end with .0')

        template = ncs.template.Template(service)
        template.apply('loopback-service-template')


class Main(ncs.application.Application):
    def setup(self):
        self.log.info('loopback-service RUNNING')
        self.register_service('loopback-service-servicepoint', ServiceCallbacks)

    def teardown(self):
        self.log.info('loopback-service FINISHED')
