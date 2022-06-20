"""
Views for the recipe APIs
"""
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from core.models import Recipe
from recipe import serializers


class RecipeViewSet(viewsets.ModelViewSet):
    """View for manage recipe APIs."""
    serializer_class = serializers.RecipeDetailSerializer
    queryset = Recipe.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve recipes for authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by('-id')

    # call method that gets called when \
    # Django Rest Framework wants to determine \
    # the class that's being used for a particular action \
    # and then overwrite behavior according to class:
    def get_serializer_class(self):
        """Return the serializer class for request."""
        if self.action == 'list':
            return serializers.RecipeSerializer

        return self.serializer_class

    # add the method to our existing RecipeViewSet \
    # in order to tell it to save the current authenticated user \
    # to the recipes that are created:
    def perform_create(self, serializer):
        """Create a new recipe."""
        serializer.save(user=self.request.user)
