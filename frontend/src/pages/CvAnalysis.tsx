
import React, { useState } from "react";
import { Upload, File, Trash2, Search, Check, X, FileText, DownloadCloud } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Badge } from "@/components/ui/badge";

interface CvFile {
  id: number;
  name: string;
  size: string;
  type: "pdf" | "docx" | "doc";
  status: "uploaded" | "analyzing" | "analyzed" | "error";
  progress?: number;
  candidate?: {
    name: string;
    email: string;
    phone: string;
    skills: { name: string; level: string; years: number }[];
    experience: { role: string; company: string; period: string }[];
    education: { degree: string; institution: string; year: string }[];
  };
}

const initialFiles: CvFile[] = [
  {
    id: 1,
    name: "sophie_martin_cv.pdf",
    size: "1.2 MB",
    type: "pdf",
    status: "analyzed",
    candidate: {
      name: "Sophie Martin",
      email: "sophie.martin@email.com",
      phone: "+33 6 12 34 56 78",
      skills: [
        { name: "React", level: "Expert", years: 5 },
        { name: "TypeScript", level: "Expert", years: 4 },
        { name: "Tailwind CSS", level: "Intermédiaire", years: 3 },
        { name: "Node.js", level: "Intermédiaire", years: 3 },
      ],
      experience: [
        { role: "Développeur Frontend Senior", company: "TechCorp", period: "2020 - Présent" },
        { role: "Développeur Frontend", company: "WebAgency", period: "2018 - 2020" },
        { role: "Développeur Web", company: "StartupXYZ", period: "2016 - 2018" },
      ],
      education: [
        { degree: "Master en Informatique", institution: "Université de Lyon", year: "2016" },
        { degree: "Licence en Informatique", institution: "Université de Lyon", year: "2014" },
      ],
    },
  },
  {
    id: 2,
    name: "thomas_bernard_resume.docx",
    size: "950 KB",
    type: "docx",
    status: "analyzing",
    progress: 65,
  },
  {
    id: 3,
    name: "emma_laurent_cv.pdf",
    size: "1.5 MB",
    type: "pdf",
    status: "uploaded",
  },
];

const CvAnalysis = () => {
  const [files, setFiles] = useState<CvFile[]>(initialFiles);
  const [selectedFile, setSelectedFile] = useState<CvFile | null>(
    initialFiles.find((file) => file.status === "analyzed") || null
  );

  const handleFileDelete = (id: number) => {
    setFiles((prevFiles) => prevFiles.filter((file) => file.id !== id));
    if (selectedFile && selectedFile.id === id) {
      setSelectedFile(null);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    // Cette fonction simule l'ajout d'un nouveau fichier
    const newFile: CvFile = {
      id: files.length + 1,
      name: "nouveau_cv.pdf",
      size: "1.1 MB",
      type: "pdf",
      status: "uploaded",
    };
    setFiles((prevFiles) => [...prevFiles, newFile]);
  };

  const handleFileSelect = (file: CvFile) => {
    setSelectedFile(file);
  };

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold tracking-tight mb-2">Analyse de CV</h1>
        <p className="text-muted-foreground">
          Téléchargez et analysez automatiquement les CV pour extraire les compétences et l'expérience.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="md:col-span-1 space-y-6">
          <Card className="border-border/40">
            <CardHeader>
              <CardTitle>Importer des CV</CardTitle>
              <CardDescription>
                Formats supportés: PDF, DOCX, DOC
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div
                className="border-2 border-dashed border-border rounded-lg p-6 text-center cursor-pointer hover:bg-accent/10 transition-colors"
                onDragOver={(e) => e.preventDefault()}
                onDrop={handleDrop}
                onClick={() => document.getElementById("file-upload")?.click()}
              >
                <Upload className="h-10 w-10 text-muted-foreground mx-auto mb-4" />
                <h3 className="text-lg font-medium mb-1">Glissez vos fichiers ici</h3>
                <p className="text-sm text-muted-foreground mb-4">
                  ou cliquez pour parcourir
                </p>
                <Button size="sm">
                  <FileText className="mr-2 h-4 w-4" />
                  Sélectionner des fichiers
                </Button>
                <input
                  type="file"
                  id="file-upload"
                  className="hidden"
                  multiple
                  accept=".pdf,.doc,.docx"
                />
              </div>
            </CardContent>
          </Card>

          <Card className="border-border/40">
            <CardHeader>
              <CardTitle>Fichiers téléchargés</CardTitle>
              <CardDescription>
                {files.length} fichiers
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {files.map((file) => (
                  <div
                    key={file.id}
                    className={`flex items-center justify-between p-3 border rounded-lg ${
                      selectedFile?.id === file.id ? "border-primary" : "border-border"
                    } hover:bg-accent/10 cursor-pointer transition-colors`}
                    onClick={() => handleFileSelect(file)}
                  >
                    <div className="flex items-center space-x-3">
                      <div className="bg-primary/20 text-primary p-2 rounded-md">
                        <File className="h-5 w-5" />
                      </div>
                      <div>
                        <p className="text-sm font-medium">{file.name}</p>
                        <p className="text-xs text-muted-foreground">{file.size}</p>
                      </div>
                    </div>
                    <div className="flex items-center space-x-2">
                      {file.status === "analyzed" && (
                        <Check className="h-4 w-4 text-green-500" />
                      )}
                      {file.status === "error" && (
                        <X className="h-4 w-4 text-red-500" />
                      )}
                      {file.status === "analyzing" && (
                        <div className="w-16 h-1">
                          <Progress value={file.progress} className="h-1" />
                        </div>
                      )}
                      <Button
                        variant="ghost"
                        size="icon"
                        onClick={(e) => {
                          e.stopPropagation();
                          handleFileDelete(file.id);
                        }}
                      >
                        <Trash2 className="h-4 w-4 text-muted-foreground hover:text-destructive" />
                      </Button>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>

        <div className="md:col-span-2">
          {selectedFile ? (
            selectedFile.status === "analyzed" && selectedFile.candidate ? (
              <Card className="border-border/40 h-full">
                <CardHeader className="flex flex-row items-center justify-between">
                  <div>
                    <CardTitle>{selectedFile.candidate.name}</CardTitle>
                    <CardDescription>
                      Données extraites du CV
                    </CardDescription>
                  </div>
                  <div className="flex items-center gap-2">
                    <Button variant="outline" size="sm">
                      <Search className="mr-1 h-4 w-4" />
                      Rechercher des offres
                    </Button>
                    <Button size="sm">
                      <DownloadCloud className="mr-1 h-4 w-4" />
                      Exporter
                    </Button>
                  </div>
                </CardHeader>
                <CardContent>
                  <Tabs defaultValue="info">
                    <TabsList className="grid grid-cols-4 mb-4">
                      <TabsTrigger value="info">Informations</TabsTrigger>
                      <TabsTrigger value="skills">Compétences</TabsTrigger>
                      <TabsTrigger value="experience">Expérience</TabsTrigger>
                      <TabsTrigger value="education">Formation</TabsTrigger>
                    </TabsList>

                    <TabsContent value="info" className="space-y-4">
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div className="space-y-1">
                          <p className="text-sm text-muted-foreground">Email</p>
                          <p>{selectedFile.candidate.email}</p>
                        </div>
                        <div className="space-y-1">
                          <p className="text-sm text-muted-foreground">Téléphone</p>
                          <p>{selectedFile.candidate.phone}</p>
                        </div>
                      </div>
                      
                      <div className="space-y-1">
                        <p className="text-sm text-muted-foreground">Résumé des compétences</p>
                        <div className="flex flex-wrap gap-1">
                          {selectedFile.candidate.skills.map((skill, idx) => (
                            <Badge key={idx} variant="secondary">
                              {skill.name} ({skill.years} ans)
                            </Badge>
                          ))}
                        </div>
                      </div>
                    </TabsContent>

                    <TabsContent value="skills" className="space-y-4">
                      <div className="space-y-4">
                        {selectedFile.candidate.skills.map((skill, idx) => (
                          <div key={idx} className="p-3 border border-border rounded-lg">
                            <div className="flex justify-between items-center">
                              <div>
                                <p className="font-medium">{skill.name}</p>
                                <p className="text-sm text-muted-foreground">
                                  {skill.years} {skill.years > 1 ? "ans" : "an"} d'expérience
                                </p>
                              </div>
                              <Badge variant={skill.level === "Expert" ? "default" : "secondary"}>
                                {skill.level}
                              </Badge>
                            </div>
                          </div>
                        ))}
                      </div>
                    </TabsContent>

                    <TabsContent value="experience" className="space-y-4">
                      <div className="space-y-4">
                        {selectedFile.candidate.experience.map((exp, idx) => (
                          <div key={idx} className="p-3 border border-border rounded-lg">
                            <p className="font-medium">{exp.role}</p>
                            <p className="text-sm">{exp.company}</p>
                            <p className="text-sm text-muted-foreground">{exp.period}</p>
                          </div>
                        ))}
                      </div>
                    </TabsContent>

                    <TabsContent value="education" className="space-y-4">
                      <div className="space-y-4">
                        {selectedFile.candidate.education.map((edu, idx) => (
                          <div key={idx} className="p-3 border border-border rounded-lg">
                            <p className="font-medium">{edu.degree}</p>
                            <p className="text-sm">{edu.institution}</p>
                            <p className="text-sm text-muted-foreground">{edu.year}</p>
                          </div>
                        ))}
                      </div>
                    </TabsContent>
                  </Tabs>
                </CardContent>
              </Card>
            ) : selectedFile.status === "analyzing" ? (
              <Card className="border-border/40 h-full flex flex-col items-center justify-center p-8 text-center">
                <div className="w-16 h-16 border-4 border-t-primary border-r-primary border-b-primary/30 border-l-primary/30 rounded-full animate-spin mb-4"></div>
                <h3 className="text-xl font-bold mb-2">Analyse en cours...</h3>
                <p className="text-muted-foreground mb-4">Extraction des informations du CV</p>
                <Progress value={selectedFile.progress} className="w-64 h-2" />
                <p className="text-sm text-muted-foreground mt-2">{selectedFile.progress}%</p>
              </Card>
            ) : (
              <Card className="border-border/40 h-full flex flex-col items-center justify-center p-8">
                <Button onClick={() => {
                  setFiles(prevFiles => 
                    prevFiles.map(file => {
                      if (file.id === selectedFile.id) {
                        return { 
                          ...file, 
                          status: "analyzing" as const,
                          progress: 0 
                        };
                      }
                      return file;
                    })
                  );
                  
                  // Simuler l'analyse
                  const timer = setInterval(() => {
                    setFiles(prevFiles => {
                      return prevFiles.map(file => {
                        if (file.id === selectedFile.id && file.status === "analyzing") {
                          const newProgress = (file.progress || 0) + 10;
                          
                          if (newProgress >= 100) {
                            clearInterval(timer);
                            return {
                              ...file,
                              status: "analyzed" as const,
                              progress: 100,
                              candidate: {
                                name: file.name.split('_').map(name => name.charAt(0).toUpperCase() + name.slice(1)).join(' ').replace(/\.\w+$/, ''),
                                email: `${file.name.split('.')[0].toLowerCase().replace(/_/g, '.')}@email.com`,
                                phone: "+33 6 " + Math.floor(10000000 + Math.random() * 90000000),
                                skills: [
                                  { name: "React", level: "Intermédiaire", years: 3 },
                                  { name: "UX Design", level: "Expert", years: 6 },
                                  { name: "Figma", level: "Expert", years: 5 },
                                  { name: "User Research", level: "Intermédiaire", years: 4 },
                                ],
                                experience: [
                                  { role: "UX Designer", company: "DesignCorp", period: "2019 - Présent" },
                                  { role: "UI Designer", company: "CreativeAgency", period: "2017 - 2019" },
                                  { role: "Graphiste", company: "StudioArt", period: "2015 - 2017" },
                                ],
                                education: [
                                  { degree: "Master en Design d'Interface", institution: "École de Design", year: "2015" },
                                  { degree: "Licence en Arts Appliqués", institution: "Université des Arts", year: "2013" },
                                ],
                              }
                            };
                          }
                          
                          return { ...file, progress: newProgress };
                        }
                        return file;
                      });
                    });
                  }, 400);
                }}>
                  <Search className="mr-2 h-4 w-4" />
                  Analyser le CV
                </Button>
              </Card>
            )
          ) : (
            <Card className="border-border/40 h-full flex flex-col items-center justify-center p-8">
              <FileText className="h-12 w-12 text-muted-foreground mb-4" />
              <h3 className="text-xl font-bold mb-2">Aucun CV sélectionné</h3>
              <p className="text-muted-foreground text-center mb-6">
                Sélectionnez un CV dans la liste pour voir les détails ou téléchargez un nouveau document pour l'analyser.
              </p>
              <Button>
                <Upload className="mr-2 h-4 w-4" />
                Télécharger un CV
              </Button>
            </Card>
          )}
        </div>
      </div>
    </div>
  );
};

export default CvAnalysis;
