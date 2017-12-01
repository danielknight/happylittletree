from bobross.models import Episode
from bobross.models import Paints
from bobross.models import User, UserArt
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.reverse import reverse
from bobross.permissions import IsOwnerOrReadOnly

from bobross.serializers import EpisodeSerializer
from bobross.serializers import PaintsSerializer
from bobross.serializers import UserSerializer, UserArtSerializer
from rest_framework.parsers import FormParser,MultiPartParser
from rest_framework import permissions
from django.http import HttpResponseRedirect, HttpResponseForbidden
from bobross.forms import UserArtForm

# Create your views here.

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'episodes': reverse('episode-list', request=request, format=format),
        'users': reverse('user-list', request=request, format=format),
        'userArt': reverse('user-art-list', request=request, format=format),
        'gallery': reverse('gallery', request=request, format=format)

    })


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserArtDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserArt.objects.all()
    serializer_class = UserArtSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class UserArtGallery(generics.ListCreateAPIView):
    queryset = UserArt.objects.all()
    serializer_class = UserArtSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    parser_classes = (MultiPartParser, FormParser,)
    renderer_classes = (TemplateHTMLRenderer,)

    def perform_create(self, serializer):
        art_file = self.request.FILES['painting']
        print(art_file)
        epi = self.request.data['episode']
        serializer.save(owner=self.request.user, painting=art_file, episode=Episode.objects.get(pk=epi))

    def get(self, request, *args, **kwargs):
        artwork = UserArt.objects.all()
        return Response({'artwork': artwork, 'nbar': 'gallery'}, template_name='bobross/gallery.html')


class UserArtList(generics.ListCreateAPIView):
    queryset = UserArt.objects.all()
    serializer_class = UserArtSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    parser_classes = (MultiPartParser, FormParser,)

    # add to perform create to upload the image
    def perform_create(self, serializer):
        art_file = self.request.FILES['painting']
        epi = self.request.data['episode']
        serializer.save(owner=self.request.user, painting=art_file, episode=Episode.objects.get(pk=epi))


class EpisodeList(generics.ListCreateAPIView):
    queryset = Episode.objects.all()
    renderer_classes = (TemplateHTMLRenderer,)
    serializer_class = EpisodeSerializer

    def get(self, request, *args, **kwargs):
        episode_list = Episode.objects.all()
        return Response({'episode_list': episode_list, 'nbar': 'episodes'}, template_name='bobross/episode_list.html')


class EpisodeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Episode.objects.all()
    renderer_classes = (TemplateHTMLRenderer,)
    serializer_class = EpisodeSerializer

    def get(self, request, pk, *args, **kwargs):
        episode = get_object_or_404(Episode, pk=pk)
        form = UserArtForm()
        return Response({'episode': episode, 'form': form, 'nbar': None}, template_name='bobross/episode.html')

    def post(self, request, pk):
        meth = request.method
        if request.method == 'POST':
            form = UserArtForm(request.POST, request.FILES)
            print(form.errors)
            if form.is_valid():
                art = UserArt()
                art.painting = form.cleaned_data['painting']
                art.episode = get_object_or_404(Episode, pk=pk)
                art.owner = self.request.user
                art.save()
                return HttpResponseRedirect(reverse("episode-detail", kwargs={'pk': pk}))
        return HttpResponseForbidden('allowed only via POST' )


class PaintsList(generics.ListCreateAPIView):
    queryset = Paints.objects.all()
    serializer_class = PaintsSerializer


class PaintDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Paints.objects.all()
    serializer_class = PaintsSerializer


class About(generics.RetrieveAPIView):
    renderer_classes = (TemplateHTMLRenderer,)

    def get(self, request, *args, **kwargs):
        return Response({'nbar': 'about'}, template_name='bobross/about.html')
