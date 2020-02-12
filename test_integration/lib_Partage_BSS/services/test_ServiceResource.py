import pytest
from lib_Partage_BSS.models import  Resource
from lib_Partage_BSS.exceptions.ServiceException import ServiceException
from lib_Partage_BSS.exceptions.NotFoundException import NotFoundException
from lib_Partage_BSS.services import AccountService, BSSConnexion, ResourceService
import time as timer

def create_account(name):
    account = AccountService.getAccount(name)
    if account == None:
        AccountService.createAccount(name,"{ssha}BIDON")

def delete_resource(name):
    resource = ResourceService.getResource(name)
    if resource != None:
        ResourceService.deleteResource(name)

def test_cleanup_bss_environment(test_config):
    print("Cleanup BSS environment before running tests...")
    #create_account(test_config['accountname'])
    #delete_resource(test_config['groupname'])

def test_createResource_cas_normal(test_config):
    newResource = ResourceService.createResource(test_config['groupname'],test_config['userPassword'],test_config['zimbraCalResType'],test_config['displayName'],password=None)
    resource = ResourceService.getResource(test_config['groupname'])
    assert resource.name == test_config['groupname']

def test_createResource_cas_resourceExistant(test_config):
    with pytest.raises(ServiceException):
        newGroup = ResourceService.createResource(test_config['groupname'],test_config['userPassword'],test_config['zimbraCalResType'],test_config['displayName'],password=None)

def test_getResource_cas_normal(test_config):
    resource = ResourceService.getResource(test_config['groupname'])
    assert resource.name == test_config['groupname']

def test_getResource_cas_resource_inexistant(test_config):
    resource = ResourceService.getResource("inexistant" + '@' + test_config['bss_domain'])
    assert resource == None

