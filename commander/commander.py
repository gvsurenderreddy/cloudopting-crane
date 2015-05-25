from flask import Flask
from flask.ext.restplus import Api, apidoc, Resource, reqparse, fields, marshal_with
from schemas import builderSchemas, clusterSchemas, composerSchemas, generalSchemas
from werkzeug.datastructures import FileStorage

app = Flask(__name__)
api = Api(app, version='0.5', title='Docker commander API',
    description='An unified API to all Docker operations.',)

# Common

errorResponseModel = api.model('Error', generalSchemas.basic_error_response)

def not_implemented():
    result = {'error':'not_implemented', 'description':'Feature not implemented yet'}
    return result, 500

def not_found():
    result = {'error':'not_found', 'description':'Resource not found'}
    return result, 404


# Build API

builder_ns = api.namespace('builder', description='Building related operations')

contextListModel = api.model('ContextList', builderSchemas.context_process_list_response)
contextInfoModel = api.model('ContextInfo', builderSchemas.context_basic_status_response)
contextDetailModel = api.model('ContextDetail', builderSchemas.context_detailed_status_response)
imageListModel = api.model('ImageList', builderSchemas.build_process_list_response)
imageInfoModel = api.model('ImageInfo', builderSchemas.build_basic_status_response)
imageDetailModel = api.model('ImageDetail', builderSchemas.build_detailed_status_response)


@builder_ns.route('/contexts')
class ContextService(Resource):
    @api.doc(description='Retrieve list of contexts.')
    @api.response(500, 'Error processing the request', errorResponseModel)
    @api.response(201, 'OK', contextListModel)
    def get(self):
        return not_implemented()

    contextArgs = api.parser()
    contextArgs.add_argument('contextName', help='Optional name for the context', location='form')
    contextArgs.add_argument('puppetfile', type=FileStorage, help='Puppetfile that indicates the puppet modules needed in the context' , location='files')
    @api.doc(description='Create new context.', parser=contextArgs)
    @api.response(500, 'Error processing the request', errorResponseModel)
    @api.response(201, 'Created', contextInfoModel)
    def post(self):
        return not_implemented()

@builder_ns.route('/contexts/<token>')
@api.doc(params={'token': 'Token that identifies the context.'})
class Context(Resource):
    @api.doc(description='Get information about a context.' )
    @api.response(500, 'Error processing the request', errorResponseModel)
    @api.response(404, 'Not found', errorResponseModel)
    @api.response(200, 'OK', contextDetailModel)
    def get(self, token):
        return not_implemented()

    @api.doc(description='Remove a context and the related data.' )
    @api.response(500, 'Error processing the request', errorResponseModel)
    @api.response(404, 'Not found', errorResponseModel)
    @api.response(200, 'OK', contextInfoModel)
    def delete(self, token):
        return not_implemented()


@builder_ns.route('/images')
class BuildService(Resource):
    @api.doc(description='Retrieve list of processes.')
    @api.response(500, 'Error processing the request', errorResponseModel)
    @api.response(201, 'OK', imageListModel)
    def get(self):
        return not_implemented()


    buildArgs = api.parser()
    buildArgs.add_argument('imageName', help='Desired image name.', location='form')
    buildArgs.add_argument('contextReference', help='Reference (context token) to the context where the image will be build. If not set it will be build in a new and empty context.', location='form')
    buildArgs.add_argument('dockerfile', type=FileStorage, help='Base image dockerfile' , location='files')
    buildArgs.add_argument('puppetmanifest', type=FileStorage, help='Puppet manifest that contains the service definition for the image.' , location='files')
    @api.doc(description='Start a build process.', parser=buildArgs)
    @api.response(500, 'Error processing the request', errorResponseModel)
    @api.response(201, 'Created', imageInfoModel)
    def post(self):
        return not_implemented()


@builder_ns.route('/images/<token>')
@api.doc(params={'token': 'Token that identifies the building process.'})
class BuildProcess(Resource):
    @api.doc(description='Get information about a build process.')
    @api.response(500, 'Error processing the request', errorResponseModel)
    @api.response(404, 'Not found', errorResponseModel)
    @api.response(200, 'OK', imageDetailModel)
    def get(self, token):
        return not_implemented()

    @api.doc(description='Remove a building process and the related data.')
    @api.response(500, 'Error processing the request', errorResponseModel)
    @api.response(404, 'Not found', errorResponseModel)
    @api.response(200, 'OK', imageInfoModel)
    def delete(self, token):
        return not_implemented()


# Cluster API

cluster_ns = api.namespace('cluster', description='Cluster related operations')

clusterInfoModel = api.model('ClusterInfo', clusterSchemas.cluster_basic_status_response)
clusterDetailModel = api.model('ClusterDetail', clusterSchemas.cluster_detailed_status_response)

machineArgs = api.parser()
machineArgs.add_argument('hostname', help='Machine hostname or IP where is accesible.', location='form')
machineArgs.add_argument('port', type=int, help='SSH port.', location='form')
machineArgs.add_argument('privateKey', type=FileStorage, help='In case of privateKey-passphrase credentials: private key with access credentials.' , location='files')
machineArgs.add_argument('passphrase', help='In case of privateKey-passphrase credentials: passphrase to decode.', location='form')
machineArgs.add_argument('user', help='In case of user-password credentials: user.', location='form')
machineArgs.add_argument('password', help='In case of user-password credentials: password.', location='form')

@cluster_ns.route('')
class ClusterService(Resource):
    @api.doc(description='Create a new swarm cluster.', parser=machineArgs)
    @api.response(500, 'Error processing the request', errorResponseModel)
    @api.response(201, 'Created', clusterInfoModel)
    def post(self):
        return not_implemented()

@cluster_ns.route('/<token>')
@api.doc(params={'token': 'Token that identifies the docker swarm cluster.'})
class ClusterInstance(Resource):
    @api.doc(description='Add a new machine to a swarm cluster.', parser=machineArgs)
    @api.response(500, 'Error processing the request', errorResponseModel)
    @api.response(404, 'Not found', errorResponseModel)
    @api.response(200, 'Created', clusterInfoModel)
    def put(self):
        return not_implemented()


    @api.doc(description='Get information about a docker swarm cluster.')
    @api.response(500, 'Error processing the request', errorResponseModel)
    @api.response(404, 'Not found', errorResponseModel)
    @api.response(200, 'OK', clusterDetailModel)
    def get(self, token):
        return not_implemented()

    @api.doc(description='Destroy a cluster and the related data.')
    @api.response(500, 'Error processing the request', errorResponseModel)
    @api.response(404, 'Not found', errorResponseModel)
    @api.response(200, 'OK', clusterInfoModel)
    def delete(self, token):
        return not_implemented()


# Composer API

composer_ns = api.namespace('composer', description='Composer related operations')

composerInfoModel = api.model('ComposerInfo', composerSchemas.composer_basic_status_response)
composerDetailModel = api.model('ComposerDetail', composerSchemas.composer_detailed_status_response)

@composer_ns.route('')
class ComposerService(Resource):
    composerArgs = api.parser()
    composerArgs.add_argument('clusterToken', help='Reference to the cluster (token used in the \'cluster\' operations).', location='form')
    composerArgs.add_argument('composefile', type=FileStorage, help='Docker-compose.yml file that specifies how to compose the service.' , location='files')
    @api.doc(description='Instance a container based service by deploying and linking the containers defined in the docker-compose.yml.', parser=composerArgs)
    @api.response(500, 'Error processing the request', errorResponseModel)
    @api.response(201, 'Created', composerInfoModel)
    def post(self):
        return not_implemented()

@composer_ns.route('/<token>')
@api.doc(params={'token': 'Token that identifies the docker composition'})
class ComposerDeployment(Resource):
    @api.doc(description='Get information about a docker container composition.')
    @api.response(500, 'Error processing the request', errorResponseModel)
    @api.response(404, 'Not found', errorResponseModel)
    @api.response(200, 'OK', composerDetailModel)
    def get(self, token):
        return not_implemented()


    @api.doc(description='Destroy the container composition and the related data.')
    @api.response(500, 'Error processing the request', errorResponseModel)
    @api.response(404, 'Not found', errorResponseModel)
    @api.response(200, 'OK', composerDetailModel)
    def delete(self, token):
        return not_implemented()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888, debug=True)
