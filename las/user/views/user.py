from .__init__ import *

@method_decorator([login_required], name='dispatch')
class UserProfile(View):
    def get(self, request):
        try:
            lasuser=User.objects.get(username=request.user.username)
            wgList=db.social.find({"@type":"WG", "users": {"$in": [request.user.username ]}})
            ### loginas ###
            hasPreviousUser = loginas.existsPreviousUser(request)
            isSuperUser = request.user.is_superuser
            return render(request, 'user/userProfile.html',{'workingGroups':wgList, 'hasPreviousUser': hasPreviousUser, 'isSuperUser': isSuperUser})
        except Exception as e:
            print ('Error profile', e)
            return redirect('/')

# mongoimport --db las --collection experiment_types  --type tsv --file list_exp.tsv --headerline
# db.experiments.insert( { name: "test_exp", genID: "ZZZ9999XXO0W00000000000000", exp_type: "Test", pipeline: "2", description: "Just some blah blah blah"} )

# {
#     name: "test_exp",
#     genID: [ "ZZZ9999XXO0W00000000000000", "CRC1331LMO0A04020004000000"],
#     exp_type: "Test",
#     pipeline: "2",
#     description: "Just some blah blah blah"
#     }
