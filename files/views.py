from user.models import *
from .models import *
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from user.serializers import *
from .serializers import *
from django.core.signing import Signer, BadSignature, TimestampSigner
from django.conf import settings
from django.http import FileResponse

signer = TimestampSigner()
class FileUploadView(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):
        if self.user.user_type!='OP':
            return Response({'detail':'Only Ops user can upload files'},status=status.HTTP_401_UNAUTHORIZED)
        file=request.Files.get('file')
        file_name = file.name

        if not file:
            return Response({"detail":"No file uploaed"},status=status.HTTP_400_BAD_REQUEST)
        try:
            serializer = FileUploadSerializer(data={'file': file, 'file_name': file_name, 'uploaded_by': request.user.username})
            if serializer.is_valid():
                serializer.save()
                return Response({'detail': 'File uploaded successfully.', 'file': serializer.data}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'detail': f'An error occurred: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

class GenerateDownloadLinkView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, file_name):
        # Ensure user is a Client User
        if request.user.user_type != 'CL':
            return Response({'detail': 'Only Client Users can access download links.'}, status=status.HTTP_403_FORBIDDEN)

        # Fetch the file by Name
        try:
            file = FileUpload.objects.get(file_name=file_name)
        except FileUpload.DoesNotExist:
            return Response({'detail': 'File not found.'}, status=status.HTTP_404_NOT_FOUND)

        token = signer.sign(file.name)  
        download_url = f"{settings.HOST_URL}/api/download/{token}"

        return Response({'download_url': download_url}, status=status.HTTP_200_OK)
    
# class DownloadFileView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request, token):
#         # Ensure user is a Client User
#         if request.user.user_type != 'CL':
#             return Response({'detail': 'Only Client Users can download files.'}, status=status.HTTP_403_FORBIDDEN)

#         try:
#             # Verify the token and get the file ID
#             file_id = signer.unsign(token, max_age=3600)  # Token expires in 1 hour
#         except BadSignature:
#             return Response({'detail': 'Invalid or expired token.'}, status=status.HTTP_400_BAD_REQUEST)

#         # Fetch the file by ID
#         try:
#             file = FileUpload.objects.get(id=file_id)
#         except FileUpload.DoesNotExist:
#             return Response({'detail': 'File not found.'}, status=status.HTTP_404_NOT_FOUND)

#         # Serve the file as a response
#         file_path = file.file.path  # Full path to the file
#         return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=file.file_name)