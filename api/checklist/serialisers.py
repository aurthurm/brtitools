from rest_framework import serializers

from apps.checklist.models import (
	Section,
	CheckList,
	Question,
	Group
)


class ChecklistSerializer(serializers.ModelSerializer):
	class Meta:
		model = CheckList
		fields = ['id', 'name', 'description', 'section', 'date_updated', 'date_created']
		read_only_fields = ['id',]

	# Enabling the serialization of section distrubs SectionSerializer ?? recursion
	# def get_fields(self):
	# 	fields = super(ChecklistSerializer, self).get_fields()
	# 	fields['section'] = SectionSerializer(many=False)
	# 	return fields


class SectionSerializer(serializers.ModelSerializer):
	checklists = ChecklistSerializer(many=True)

	class Meta:
		model = Section
		fields = ['id', 'name', 'description', 'checklists']
		read_only_fields = ['id',]



class GroupSerializer(serializers.ModelSerializer):
	class Meta:
		model = Group
		fields = ['id' ,'name', 'question',]


class QuestionSerializer(serializers.ModelSerializer):
	class Meta:
		model = Question
		fields = [
			'id', 'checklist', 'question', 
			'category', 'required', 'number',
			'parent','children', 'help', 'group', 'groups',
			'get_admin_change_url',
		]

	def get_fields(self):
		fields = super(QuestionSerializer, self).get_fields()
		fields['checklist'] = ChecklistSerializer(many=False)
		fields['children'] = QuestionSerializer(many=True)
		fields['group'] = GroupSerializer(many=False)
		fields['groups'] = GroupSerializer(many=True)
		return fields
