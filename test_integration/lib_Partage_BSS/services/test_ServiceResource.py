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
    delete_resource(test_config['groupname'])

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

def test_modifyResource_cas_Normal(test_config):
    resource_as_dict = { 'displayName': "TestName",
                        'postalCode': "00000555",
                        'zimbraCalResAutoDeclineIfBusy': "FALSE",
                        'zimbraCalResContactEmail': "contact@x.fr",
                        'l': "Rennes"
                        }
    resource = ResourceService.getResource(test_config['groupname'])
    for attribute in resource_as_dict:
        setattr(resource, "_" + attribute, resource_as_dict[attribute])
    ResourceService.modifyResource(resource)
    resource = ResourceService.getResource(test_config['groupname'])
    errors = 0
    for attribute in resource_as_dict:
        if getattr(resource, "_" + attribute) != resource_as_dict[attribute]:
            errors = errors + 1
    assert errors == 0

def test_modifyResource_cas_addZimbraPrefCalendarForwardInvitesTo(test_config):
    resource = ResourceService.getResource(test_config['groupname'])
    resource.addZimbraPrefCalendarForwardInvitesTo("resource@x.fr")
    ResourceService.modifyResource(resource)
    resource = ResourceService.getResource(test_config['groupname'])


    assert "resource@x.fr" in resource.zimbraPrefCalendarForwardInvitesTo


def test_modifyResource_cas_addZimbraPrefCalendarForwardInvitesToCompteErrone(test_config):
    resource = ResourceService.getResource(test_config['groupname'])
    resource.addZimbraPrefCalendarForwardInvitesTo("resourcettx.fr")
    ResourceService.modifyResource(resource)
    resource = ResourceService.getResource(test_config['groupname'])

    assert "resourcettx.fr" not in resource.zimbraPrefCalendarForwardInvitesTo

def test_modifyResource_cas_removeZimbraPrefCalendarForwardInvitesTo(test_config):
    resource = ResourceService.getResource(test_config['groupname'])
    resource.removeZimbraPrefCalendarForwardInvitesTo("resource@x.fr")
    ResourceService.modifyResource(resource)
    resource1 = ResourceService.getResource(test_config['groupname'])
    assert "resource@x.fr" not in resource1.zimbraPrefCalendarForwardInvitesTo

def test_deleteResource_cas_normal(test_config):
    newResource = ResourceService.deleteResource(test_config['groupname'])
    resource = ResourceService.getResource(test_config['groupname'])
    assert resource == None

def test_deleteResource_cas_resource_inexistant(test_config):
    with pytest.raises(ServiceException):
        resource = ResourceService.deleteResource(test_config['groupname'])
