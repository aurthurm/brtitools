from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404

from rest_framework import generics, mixins, permissions
from rest_framework.views import APIView
from rest_framework.response import Response

from .serialisers import (
	SectionSerializer,
	ChecklistSerializer,
	QuestionSerializer,
	GroupSerializer
)

from apps.checklist.models import (
	Section,
	CheckList,
	Question,
)

User = get_user_model()


class SectionListAPIView(generics.ListAPIView):
	serializer_class = SectionSerializer
	permission_classes = (permissions.AllowAny,)

	def get_queryset(self):        
	    queryset = Section.objects.exclude()
	    return queryset


class SectionCreateAPIView(generics.CreateAPIView):
	serializer_class = SectionSerializer
	permission_classes = (permissions.AllowAny,)
	
	def post(self, request, *args, **kwargs):
		name = request.data.get('name')
		description = request.data.get('description')
		section = None
		if name:
			sections = Section.objects.filter(name__exact=name)
			if sections.count() > 0:
				message = "A checklist with that name already exists"
				return Response({'error': message})
			else:
				section = Section.objects.create(
					name=name,
					description=description
				)
				serializer = SectionSerializer(section)
				return Response(serializer.data)
		return Response({'error': "Error!!!: Provide a name"})


class ChecklistListAPIView(generics.ListAPIView):
	"""
	Displays checklists already categorised by sections
	"""
	serializer_class = ChecklistSerializer
	permission_classes = (permissions.AllowAny,)

	def get_queryset(self):        
	    queryset = CheckList.objects.exclude()		
	    return queryset


class ChecklistCreateRetrieveAPIView(generics.CreateAPIView, mixins.RetrieveModelMixin):
	serializer_class = ChecklistSerializer
	permission_classes = (permissions.AllowAny,)

	def get(self, request, *args, **kwargs):
		"""
		Not working
		"""
		checklist_id = request.GET.get('id', None)
		checklist = None
		if checklist_id:
			try:
				checklist = get_object_or_404(CheckList, pk=checklist_id)
			except Exception as e:
				return Response({'error': f"{str(e)}"})
			
		serializer = ChecklistSerializer(checklist)
		return Response({'checklist': serializer.data})

	def post(self, request, *args, **kwargs):
		name = request.data.get('name')
		description = request.data.get('description')
		section_id = request.data.get('sectionId')
		if not section_id:
			return Response({'error': "Error!!!: select a Section"})
		section = get_object_or_404(Section, pk=section_id)
		if name and section:
			checklists = CheckList.objects.filter(name__exact=name.strip())
			if checklists.count() > 0:
				message = "A checklist with that name already exists"
				return Response({'error': message})
			else:
				checklist = CheckList.objects.create(
						name=name,
						description=description,
						section=section,
						need_logged_user=False,
						editable_answers=True,
						is_published=True
					)
				serializer = ChecklistSerializer(checklist)
				return Response(serializer.data)
		return Response({'error': "Error!!!: Provide a name, description and a valid section"})


class QuestionListAPIView(generics.ListAPIView):
	serializer_class = QuestionSerializer
	permission_classes = (permissions.AllowAny,)

	def get_queryset(self):
		checklist_id = self.request.GET.get('checklist_id', None)  
		queryset = Question.objects.all()
		if checklist_id:
			queryset = queryset.filter(checklist_id__exact=checklist_id)
		return queryset


class QuestionCreateAPIView(generics.CreateAPIView):
	serializer_class = QuestionSerializer
	permission_classes = (permissions.AllowAny,)

	def questionSetter(self, _data):
		fields = [
			"checklist", "question", "category", "required", 
			"number", "has_sub_questions", "has_sub_questions_grouped", 
			"parent", "children", "help","group"
		]
		representation = dict()
		for field in fields:
			if field == "chidren":
				representation[field] = []
				_children = _data.get(field, None)
				if _children:
					for child in list(_children):
						representation[field].append(self.questionSetter(child))
			else:
				representation[field] = _data.get(field, None)
		return representation

	def post(self, *args, **kwargs):
		data = self.questionSetter(self.request.POST)
		return Response({})
		

class GroupAPIView(generics.ListCreateAPIView):
	serializer_class = GroupSerializer



